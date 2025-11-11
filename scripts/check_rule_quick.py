from rule_based import RuleBasedSentiment

rb = RuleBasedSentiment()

path = "failed_patterns.txt"

with open(path, encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

print(f"Checking {min(50, len(lines))} failed patterns with rule-based analyzer\n")
for ln in lines[:50]:
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
