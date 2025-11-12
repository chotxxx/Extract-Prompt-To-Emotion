import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rule_based import RuleBasedSentiment
from fusion import ConditionalFusion
from phobert_module import PhoBERTModule

# List of prompts with expected sentiments (no diacritics)
test_prompts = [
    ("Hom nay toi rat vui", "POSITIVE"),
    ("Mon an nay do qua", "NEGATIVE"),
    ("Hom nay toi cam thay binh thuong", "NEUTRAL"),
    ("Rat vui hom nay", "POSITIVE"),
    ("Cong viec nay khien toi on dinh", "NEUTRAL"),
    ("Phim nay hay lam", "POSITIVE"),
    ("Toi buon vi that bai", "NEGATIVE"),
    ("Ngay mai di hoc", "NEUTRAL"),
    ("Cam on ban rat nhieu", "POSITIVE"),
    ("Met moi qua hom nay", "NEGATIVE"),
]

def test_no_diacritic_prompts():
    rb = RuleBasedSentiment()
    fu = ConditionalFusion()
    phobert = PhoBERTModule()

    print("Testing 10 prompts without diacritics (no-diacritic versions):")
    print("=" * 60)

    for text, expected in test_prompts:
        # Get predictions
        l_phobert, c_phobert = phobert.analyze_sentiment(text)
        s_rule = rb.analyze_sentiment(text)
        mixed_flag = rb.detect_mixed_sentiment(text)
        neutral_flag = rb.is_neutral_context(text)
        l_fusion, _ = fu.fuse(l_phobert, c_phobert, s_rule, mixed_flag=mixed_flag, neutral_flag=neutral_flag)

        # Check if fusion matches expected
        match = "✓" if l_fusion == expected else "✗"

        print(f"Text: {text}")
        print(f"  Expected: {expected}")
        print(f"  Fusion: {l_fusion} {match}")
        print(f"  PhoBERT: {l_phobert} ({c_phobert:.2f})")
        print(f"  Rule: {rb.get_label(s_rule)} ({s_rule:.2f})")
        print()

if __name__ == '__main__':
    test_no_diacritic_prompts()