import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from validation import validate_input
from phobert_module import PhoBERTModule
from rule_based import RuleBasedSentiment
from fusion import ConditionalFusion

def read_prompts(file_path):
    prompts = []
    labels = []
    with open(file_path, encoding='utf-8') as f:
        current_label = None
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):  # Skip comments/empty
                if 'Positive' in line:
                    current_label = 'POSITIVE'
                elif 'Negative' in line:
                    current_label = 'NEGATIVE'
                elif 'Neutral' in line:
                    current_label = 'NEUTRAL'
                continue
            prompts.append(line)
            labels.append(current_label)
    return prompts, labels

def read_prompts_combined():
    prompts = []
    labels = []
    # Read refined (có dấu, tab-separated)
    with open(os.path.join('test', 'test_1000_prompts_refined.txt'), encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if '\t' in line:
                text, label = line.split('\t')
                prompts.append(text)
                labels.append(label.strip().upper())
    # Read không dấu (grouped by label)
    with open(os.path.join('test', 'test_1000_prompts_khong_dau.txt'), encoding='utf-8') as f:
        current_label = None
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                if 'Positive' in line:
                    current_label = 'POSITIVE'
                elif 'Negative' in line:
                    current_label = 'NEGATIVE'
                elif 'Neutral' in line:
                    current_label = 'NEUTRAL'
                continue
            prompts.append(line)
            labels.append(current_label)
    return prompts, labels

def test_prompts(prompts, labels):
    correct = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    total = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    for text, label in zip(prompts, labels):
        is_valid, _ = validate_input(text)
        # For this test, we only check if input is valid (should always be True)
        # You can add sentiment prediction here if needed
        if is_valid:
            correct[label] += 1
        total[label] += 1
    return correct, total

def test_hybrid(prompts, labels):
    phobert = PhoBERTModule()
    rule = RuleBasedSentiment()
    fusion = ConditionalFusion()
    correct_phobert = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    correct_rule = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    correct_fusion = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    total = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    for text, label in zip(prompts, labels):
        is_valid, _ = validate_input(text)
        if not is_valid:
            continue
        l_phobert, c_phobert = phobert.analyze_sentiment(text)
        s_rule = rule.analyze_sentiment(text)
        mixed_flag = rule.detect_mixed_sentiment(text)
        neutral_flag = rule.is_neutral_context(text)
        l_rule = rule.get_label(s_rule)
        l_fusion, _ = fusion.fuse(l_phobert, c_phobert, s_rule, mixed_flag=mixed_flag, neutral_flag=neutral_flag)
        if l_phobert == label:
            correct_phobert[label] += 1
        if l_rule == label:
            correct_rule[label] += 1
        if l_fusion == label:
            correct_fusion[label] += 1
        total[label] += 1
    return correct_phobert, correct_rule, correct_fusion, total

def main():
    prompts, labels = read_prompts_combined()
    correct_phobert, correct_rule, correct_fusion, total = test_hybrid(prompts, labels)
    print('--- Hybrid Model Accuracy (Combined) ---')
    failed_patterns = []
    phobert = PhoBERTModule()
    rule = RuleBasedSentiment()
    fusion = ConditionalFusion()
    for text, label in zip(prompts, labels):
        is_valid, _ = validate_input(text)
        if not is_valid:
            continue
        l_phobert, c_phobert = phobert.analyze_sentiment(text)
        s_rule = rule.analyze_sentiment(text)
        mixed_flag = rule.detect_mixed_sentiment(text)
        neutral_flag = rule.is_neutral_context(text)
        l_fusion, _ = fusion.fuse(l_phobert, c_phobert, s_rule, mixed_flag=mixed_flag, neutral_flag=neutral_flag)
        if l_fusion != label:
            failed_patterns.append((text, label, l_fusion, l_phobert, rule.get_label(s_rule)))
    with open('failed_patterns.txt', 'w', encoding='utf-8') as f:
        for item in failed_patterns:
            f.write(f'{item[0]}\tGT:{item[1]}\tFusion:{item[2]}\tPhoBERT:{item[3]}\tRule:{item[4]}\n')
    for label in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
        acc_p = correct_phobert[label] / total[label] * 100 if total[label] else 0
        acc_r = correct_rule[label] / total[label] * 100 if total[label] else 0
        acc_f = correct_fusion[label] / total[label] * 100 if total[label] else 0
        print(f'{label}: PhoBERT={acc_p:.2f}% | Rule={acc_r:.2f}% | Fusion={acc_f:.2f}%')
    print(f'Total Fusion: {sum(correct_fusion.values())}/{sum(total.values())} = {sum(correct_fusion.values())/sum(total.values())*100:.2f}%')
    print(f'Failed patterns saved to failed_patterns.txt ({len(failed_patterns)} samples)')

if __name__ == '__main__':
    main()
