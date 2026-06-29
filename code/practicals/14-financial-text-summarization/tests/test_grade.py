from tools._common import load_filing_text
from tools.grade import faithfulness, figure_coverage, grade, unsupported_figures

SOURCE = load_filing_text()

# A summary that uses only figures the extractor found in the filing.
FAITHFUL = (
    "Orion Dynamics reported revenue of $1.46 billion, a gross margin of 58%, and "
    "diluted EPS of $1.27. It raised full-year revenue guidance to a range of "
    "$5.90 billion to $6.10 billion."
)

# A summary with invented figures (2.30, 73, 4.10) and invented claims absent from the filing.
INVENTED = (
    "Orion Dynamics posted revenue of $2.30 billion, a gross margin of 73%, and "
    "diluted EPS of $4.10. Management warned of a goodwill writedown in Brazil and "
    "suspended its buyback program amid a regulatory probe in Singapore."
)


def test_faithful_summary_scores_high():
    assert faithfulness(FAITHFUL, SOURCE) >= 0.8


def test_invented_summary_scores_much_lower():
    assert faithfulness(INVENTED, SOURCE) < 0.5 < faithfulness(FAITHFUL, SOURCE)


def test_figure_coverage_flags_invented_numbers():
    assert figure_coverage(FAITHFUL, SOURCE) == 1.0
    assert figure_coverage(INVENTED, SOURCE) < 1.0
    bad = unsupported_figures(INVENTED, SOURCE)
    assert "73" in bad and "2.30" in bad and "4.10" in bad


def test_grade_verdict():
    assert grade(FAITHFUL, SOURCE)["supported"] is True
    assert grade(INVENTED, SOURCE)["supported"] is False
