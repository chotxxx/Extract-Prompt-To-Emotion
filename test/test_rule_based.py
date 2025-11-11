import unittest
from rule_based import RuleBasedSentiment

class TestRuleBasedHelpers(unittest.TestCase):
    def setUp(self):
        self.rb = RuleBasedSentiment()

    def test_detect_mixed_sentiment(self):
        text = "Tôi thích nó lắm tuy nhiên khủng khiếp"
        self.assertTrue(self.rb.detect_mixed_sentiment(text))

    def test_post_contrast_clause_score(self):
        text = "Sản phẩm rất tốt nhưng tồi tệ"
        post = self.rb._post_contrast_clause_score(text)
        self.assertLess(post, 0, msg=f"Expected negative post-contrast score, got {post}")

    def test_is_neutral_context_question(self):
        text = "Bạn nghĩ tôi sẽ mua lại sản phẩm này?"
        self.assertTrue(self.rb.is_neutral_context(text))

    def test_detect_added_negative_phrase(self):
        # phrase we recently added
        text = "Giá cả quá cao"
        score = self.rb.analyze_sentiment(text)
        self.assertLess(score, 0, msg=f"Expected negative score for 'Giá cả quá cao', got {score}")

if __name__ == '__main__':
    unittest.main()
