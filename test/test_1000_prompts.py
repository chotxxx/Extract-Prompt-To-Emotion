import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing import VietnamesePreprocessor
# from phobert_module import PhoBERTModule
from rule_based import RuleBasedSentiment
# from fusion import ConditionalFusion

def load_test_prompts(filename="test_1000_prompts_refined.txt"):
    prompts = []
    # Use the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            text, label = line.strip().split("\t")
            prompts.append((text, label))
    return prompts

def evaluate_1000_prompts():
    preprocessor = VietnamesePreprocessor()
    # phobert = PhoBERTModule()
    rule_based = RuleBasedSentiment()
    # fusion = ConditionalFusion()

    prompts = load_test_prompts()
    correct = 0
    total = len(prompts)

    category_stats = {"POSITIVE": {"correct": 0, "total": 0},
                     "NEGATIVE": {"correct": 0, "total": 0},
                     "NEUTRAL": {"correct": 0, "total": 0}}

    print(f"Evaluating on {total} diverse prompts:")

    for i, (text, expected) in enumerate(prompts):
        processed = preprocessor.preprocess(text)
        processed_no_seg = preprocessor.remove_noise(text)
        processed_no_seg = preprocessor.normalize_teencode(processed_no_seg)
        # l_phobert, c_phobert = phobert.analyze_sentiment(processed)
        s_rule = rule_based.analyze_sentiment(processed_no_seg)
        # final_label, _ = fusion.fuse(l_phobert, c_phobert, s_rule)
        
        # For now, just use rule-based score to determine label
        if s_rule >= 0.8:
            final_label = "POSITIVE"
        elif s_rule <= -0.5:
            final_label = "NEGATIVE"
        else:
            final_label = "NEUTRAL"

        category_stats[expected]["total"] += 1
        if final_label == expected:
            correct += 1
            category_stats[expected]["correct"] += 1
        else:
            if i < 20:  # Show first 20 failures
                print(f"Case {i+1}: FAIL - Text: '{text}' - Expected: {expected}, Got: {final_label} (Rule: {s_rule})")

    accuracy = correct / total * 100
    print(f"\nOverall Accuracy on 1000 prompts: {accuracy:.2f}%")

    print("\nCategory-wise Accuracy:")
    for cat, stats in category_stats.items():
        if stats["total"] > 0:
            cat_acc = stats["correct"] / stats["total"] * 100
            print(f"{cat}: {cat_acc:.2f}% ({stats['correct']}/{stats['total']})")

if __name__ == "__main__":
    evaluate_1000_prompts()