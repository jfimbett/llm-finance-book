from tools._common import load_source, load_target
from tools.check import passes
from tools.metric import score

SOURCE = load_source()
TARGET = load_target()

BELOW = (  # 3 of 5 facts -> coverage 0.6
    "Revenue rose 22% to 2.4 billion dollars. Operating margin expanded to 17%. "
    "Order backlog reached 3.1 billion dollars."
)
AT_THRESHOLD = BELOW + " Free cash flow of 310 million dollars."  # 4 of 5 -> coverage 0.8
ABOVE = AT_THRESHOLD + " Guidance for fiscal 2026 was issued."     # 5 of 5 -> coverage 1.0


def test_gate_fails_below_threshold():
    assert passes(score(BELOW, SOURCE, TARGET)) is False


def test_gate_passes_exactly_at_threshold():
    report = score(AT_THRESHOLD, SOURCE, TARGET)
    assert report["coverage"] == report["threshold"]
    assert passes(report) is True


def test_gate_passes_above_threshold():
    assert passes(score(ABOVE, SOURCE, TARGET)) is True


def test_gate_rejects_unfaithful_draft_even_at_full_coverage():
    draft = ABOVE + " A surprise segment posted a 45% margin."
    report = score(draft, SOURCE, TARGET)
    assert report["coverage"] == 1.0
    assert passes(report) is False  # faithful is False -> target not met
