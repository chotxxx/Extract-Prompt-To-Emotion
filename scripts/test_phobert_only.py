import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from phobert_module import PhoBERTModule

def load_test_prompts(filename="test_1000_random_prompts.txt"):
    prompts = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            text, label = line.strip().split("\t")
            prompts.append((text, label))
    return prompts

def test_phobert_only():
    phobert = PhoBERTModule()

    prompts = load_test_prompts()
    correct = 0
    total = len(prompts)

    category_stats = {"POSITIVE": {"correct": 0, "total": 0},
                     "NEGATIVE": {"correct": 0, "total": 0},
                     "NEUTRAL": {"correct": 0, "total": 0}}

    print(f"Testing PhoBERT only on {total} random prompts:")

    failed_cases = []

    for i, (text, expected) in enumerate(prompts):
        # Get PhoBERT prediction
        l_phobert, c_phobert = phobert.analyze_sentiment(text)

        category_stats[expected]["total"] += 1
        if l_phobert == expected:
            correct += 1
            category_stats[expected]["correct"] += 1
        else:
            failed_cases.append((text, expected, l_phobert, c_phobert))
            if len(failed_cases) <= 20:  # Show first 20 failures
                print(f"Case {i+1}: FAIL - Text: '{text}' - Expected: {expected}, Got: {l_phobert} ({c_phobert:.2f})")

    # Save all failed cases to file
    with open("failed_phobert_only.txt", "w", encoding="utf-8") as f:
        for text, expected, got, conf in failed_cases:
            f.write(f"{text}\t{expected}\t{got}\t{conf:.2f}\n")

    print(f"\nSaved {len(failed_cases)} failed cases to failed_phobert_only.txt")

    accuracy = correct / total * 100
    print(f"\nPhoBERT Only Accuracy on 1000 random prompts: {accuracy:.2f}%")

    print("\nCategory-wise Accuracy:")
    for cat, stats in category_stats.items():
        if stats["total"] > 0:
            cat_acc = stats["correct"] / stats["total"] * 100
            print(f"{cat}: {cat_acc:.2f}% ({stats['correct']}/{stats['total']})")

if __name__ == '__main__':
    test_phobert_only()