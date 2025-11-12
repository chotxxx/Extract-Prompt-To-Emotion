import sys
import os

# Ensure repo root is on sys.path so top-level modules can be imported when
# this script is executed from the scripts/ folder.
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
if REPO_ROOT not in sys.path:
	sys.path.insert(0, REPO_ROOT)

from preprocessing import VietnamesePreprocessor
from phobert_module import PhoBERTModule
from rule_based import RuleBasedSentiment
from fusion import ConditionalFusion

text = "Sản phẩm này tương đối ổn thôi"
print("Input:", text)

pre = VietnamesePreprocessor()
ph = PhoBERTModule()
rb = RuleBasedSentiment()
fus = ConditionalFusion()

processed = pre.preprocess(text)
print("Processed:", processed)

l_phobert, c_phobert = ph.analyze_sentiment(processed)
print(f"PhoBERT -> Label: {l_phobert}, Confidence: {c_phobert:.4f}")

s_rule = rb.analyze_sentiment(processed)
print(f"Rule score: {s_rule:.4f}, Rule label: {rb.get_label(s_rule)}")

mixed = rb.detect_mixed_sentiment(processed)
neutral = rb.is_neutral_context(processed)
hedged = rb.is_hedged(processed)
print(f"Flags -> mixed: {mixed}, neutral: {neutral}, hedged: {hedged}")

final_label, final_conf = fus.fuse(l_phobert, c_phobert, s_rule, mixed_flag=mixed, neutral_flag=neutral, hedged_flag=hedged)
print(f"Fusion -> Final Label: {final_label}, Final Confidence: {final_conf:.4f}")
