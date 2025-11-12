import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rule_based import RuleBasedSentiment
from fusion import ConditionalFusion
from phobert_module import PhoBERTModule

def load_test_prompts(filename="test_1000_random_prompts.txt"):
    prompts = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            text, label = line.strip().split("\t")
            prompts.append((text, label))
    return prompts

def test_random_1000_prompts():
    rb = RuleBasedSentiment()
    fu = ConditionalFusion()
    phobert = PhoBERTModule()

    prompts = load_test_prompts()
    correct = 0
    total = len(prompts)

    category_stats = {"POSITIVE": {"correct": 0, "total": 0},
                     "NEGATIVE": {"correct": 0, "total": 0},
                     "NEUTRAL": {"correct": 0, "total": 0}}

    print(f"Testing on {total} random prompts:")

    failed_cases = []

    for i, (text, expected) in enumerate(prompts):
        # Get predictions
        l_phobert, c_phobert = phobert.analyze_sentiment(text)
        s_rule = rb.analyze_sentiment(text)
        mixed_flag = rb.detect_mixed_sentiment(text)
        neutral_flag = rb.is_neutral_context(text)
        l_fusion, _ = fu.fuse(l_phobert, c_phobert, s_rule, mixed_flag=mixed_flag, neutral_flag=neutral_flag)

        category_stats[expected]["total"] += 1
        if l_fusion == expected:
            correct += 1
            category_stats[expected]["correct"] += 1
        else:
            failed_cases.append((text, expected, l_fusion, l_phobert, c_phobert, rb.get_label(s_rule), s_rule))
            if len(failed_cases) <= 20:  # Show first 20 failures
                print(f"Case {i+1}: FAIL - Text: '{text}' - Expected: {expected}, Got: {l_fusion} (PhoBERT: {l_phobert} {c_phobert:.2f}, Rule: {rb.get_label(s_rule)} {s_rule:.2f})")

    # Save all failed cases to file
    with open("failed_random_1000.txt", "w", encoding="utf-8") as f:
        for text, expected, got, pho_l, pho_c, rule_l, rule_s in failed_cases:
            f.write(f"{text}\t{expected}\t{got}\t{pho_l}\t{pho_c:.2f}\t{rule_l}\t{rule_s:.2f}\n")

    print(f"\nSaved {len(failed_cases)} failed cases to failed_random_1000.txt")

    accuracy = correct / total * 100
    print(f"\nOverall Accuracy on 1000 random prompts: {accuracy:.2f}%")

    print("\nCategory-wise Accuracy:")
    for cat, stats in category_stats.items():
        if stats["total"] > 0:
            cat_acc = stats["correct"] / stats["total"] * 100
            print(f"{cat}: {cat_acc:.2f}% ({stats['correct']}/{stats['total']})")

if __name__ == '__main__':
    test_random_1000_prompts()