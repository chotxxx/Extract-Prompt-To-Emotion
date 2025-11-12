import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rule_based import RuleBasedSentiment
from fusion import ConditionalFusion
from phobert_module import PhoBERTModule


def load_test_prompts(filename=None):
    prompts = []
    import os
    if filename is None:
        ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        filename = os.path.join(ROOT, 'test_100_mixed_prompts.txt')

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                text, label = parts[0], parts[1]
                prompts.append((text, label))
    return prompts


def test_mixed_prompts():
    rb = RuleBasedSentiment()
    fu = ConditionalFusion()
    phobert = PhoBERTModule()

    prompts = load_test_prompts()
    correct = 0
    total = len(prompts)

    failed_cases = []

    for i, (text, expected) in enumerate(prompts):
        l_phobert, c_phobert = phobert.analyze_sentiment(text)
        s_rule = rb.analyze_sentiment(text)
        mixed_flag = rb.detect_mixed_sentiment(text)
        neutral_flag = rb.is_neutral_context(text)
        l_fusion, conf = fu.fuse(l_phobert, c_phobert, s_rule, mixed_flag=mixed_flag, neutral_flag=neutral_flag)

        if l_fusion == expected:
            correct += 1
        else:
            failed_cases.append((text, expected, l_fusion, l_phobert, c_phobert, rb.get_label(s_rule), s_rule))
            if len(failed_cases) <= 30:
                print(f"Case {i+1}: FAIL - '{text}' - Expected: {expected}, Got: {l_fusion} (PhoBERT: {l_phobert} {c_phobert:.2f}, Rule: {rb.get_label(s_rule)} {s_rule:.2f})")

    # Save failures
    with open("failed_mixed_100.txt", "w", encoding="utf-8") as f:
        for text, expected, got, pho_l, pho_c, rule_l, rule_s in failed_cases:
            f.write(f"{text}\t{expected}\t{got}\t{pho_l}\t{pho_c:.2f}\t{rule_l}\t{rule_s:.2f}\n")

    acc = correct / total * 100 if total > 0 else 0.0
    print(f"\nTested {total} prompts. Accuracy: {acc:.2f}% ({correct}/{total})")
    print(f"Saved {len(failed_cases)} failed cases to failed_mixed_100.txt")

if __name__ == '__main__':
    test_mixed_prompts()
