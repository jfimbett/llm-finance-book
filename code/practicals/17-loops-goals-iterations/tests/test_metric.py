from tools._common import load_source, load_target
from tools.metric import coverage, missing_facts, score, unsupported_figures

SOURCE = load_source()
TARGET = load_target()
FACTS = TARGET["facts"]

# A draft built up one required fact at a time. Every figure used appears in the source,
# so each step stays faithful; only coverage changes.
STEPS = [
    "Meridian Robotics reported full-year results.",
    " Revenue rose 22% to 2.4 billion dollars.",
    " Operating margin expanded to 17% from 13%.",
    " Order backlog reached 3.1 billion dollars.",
    " Free cash flow of 310 million dollars.",
    " Management issued guidance for fiscal 2026.",
]


def _cumulative():
    text = ""
    for piece in STEPS:
        text += piece
        yield text


def test_coverage_rises_as_missing_facts_are_added():
    cov = [coverage(c, FACTS) for c in _cumulative()]
    assert cov[0] == 0.0
    assert cov[-1] == 1.0
    # strictly monotonic: each added fact lifts the score
    assert all(b > a for a, b in zip(cov, cov[1:])), cov


def test_missing_fact_is_flagged_below_target():
    # covers revenue + margin + backlog only (3 of 5) -> below the 0.8 threshold
    draft = (
        "Revenue rose 22% to 2.4 billion dollars. Operating margin expanded to 17%. "
        "Order backlog reached 3.1 billion dollars."
    )
    report = score(draft, SOURCE, TARGET)
    assert report["coverage"] < report["threshold"]
    missing_ids = {f["id"] for f in report["missing"]}
    assert missing_ids == {"fcf", "guidance"}


def test_fabricated_figure_breaks_faithfulness():
    # fully covers every fact, but invents a margin of 45% that is not in the source
    draft = (
        "Revenue rose 22% to 2.4 billion dollars. Operating margin expanded to 17%, "
        "with a one-off division at 45%. Order backlog reached 3.1 billion dollars. "
        "Free cash flow of 310 million dollars. Guidance for fiscal 2026 was issued."
    )
    report = score(draft, SOURCE, TARGET)
    assert report["coverage"] == 1.0
    assert report["faithful"] is False
    assert "45%" in report["unsupported_figures"]


def test_faithful_full_summary_uses_only_source_figures():
    full = "".join(STEPS)
    assert unsupported_figures(full, SOURCE) == []
    assert missing_facts(full, FACTS) == []
