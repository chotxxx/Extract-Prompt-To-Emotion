import pytest

from rule_based import RuleBasedSentiment


@pytest.fixture()
def rb():
    return RuleBasedSentiment()


def test_detect_cung_mixed(rb):
    # Hedged mixed example should be detected as mixed
    text = "Hôm nay không vui cũng không buồn"
    assert rb.detect_mixed_sentiment(text) is True


def test_analyze_cung_returns_neutral(rb):
    # After detection, analyze_sentiment should neutralize ambiguous "cũng" patterns
    text = "Hôm nay không vui cũng không buồn"
    score = rb.analyze_sentiment(text)
    assert score == 0.0


def test_detect_cung_positive_both_sides(rb):
    # Even if both sides are positive, the heuristic flags the structure as mixed/ambiguous
    text = "Hôm nay vui cũng vui"
    assert rb.detect_mixed_sentiment(text) is True
