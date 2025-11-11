import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("rbmod", Path("rule_based.py").resolve())
rbmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rbmod)

RuleBasedSentiment = rbmod.RuleBasedSentiment
rb = RuleBasedSentiment()

path = Path("failed_patterns.txt")
if not path.exists():
    print("failed_patterns.txt not found in repo root")
    raise SystemExit(1)

lines = [l.strip() for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]
print(f"Checking {min(60, len(lines))} failed patterns with rule-based analyzer\n")
for ln in lines[:60]:
    parts = ln.split('\t')
    text = parts[0]
    gt = parts[1] if len(parts) > 1 else "GT:UNKNOWN"
    score = rb.analyze_sentiment(text)
    label = rb.get_label(score)
    mixed = rb.detect_mixed_sentiment(text)
    post = rb._post_contrast_clause_score(text)
    print(f"TEXT: {text}")
    print(f"  GT: {gt} | rule_score={score:.2f} | rule_label={label} | mixed={mixed} | post_contrast_score={post:.2f}")
    print()
