# Generate 100 mixed/hedge Vietnamese prompts (neutral-ish patterns)
# Writes to ../test_100_mixed_prompts.txt with format: <text>\t<EXPECTED_LABEL>

adjs = [
    "vui",
    "buồn",
    "ổn",
    "tốt",
    "tệ",
    "hài lòng",
    "thất vọng",
    "khó chịu",
    "bình thường",
    "hạnh phúc",
]

neg_forms = ["", "không "]

templates = [
    "Hôm nay {a1}{adj1} cũng {a2}{adj2}",
    "Hôm nay {a1}{adj1}, cũng {a2}{adj2}",
    "Hôm nay {a1}{adj1} nhưng cũng {a2}{adj2}",
    "Hôm nay {a1}{adj1} và {a2}{adj2}",
    "Hôm nay nhìn chung {a1}{adj1} cũng {a2}{adj2}",
]

prompts = []
seen = set()

# Produce combinations, prioritize mixed/ambiguous patterns
for t in templates:
    for adj1 in adjs:
        for adj2 in adjs:
            for a1 in neg_forms:
                for a2 in neg_forms:
                    # Keep some variety but avoid identical full repeats unless requested
                    text = t.format(a1=a1, adj1=adj1, a2=a2, adj2=adj2)
                    text = text.strip()
                    if len(prompts) >= 100:
                        break
                    # Avoid exact duplicates
                    if text.lower() in seen:
                        continue
                    seen.add(text.lower())
                    # We'll mark expected label as NEUTRAL for these hedge/mixed patterns
                    prompts.append((text, "NEUTRAL"))
                if len(prompts) >= 100:
                    break
            if len(prompts) >= 100:
                break
        if len(prompts) >= 100:
            break
    if len(prompts) >= 100:
        break

# If not enough generated (unlikely), fill with random combos
if len(prompts) < 100:
    import random
    while len(prompts) < 100:
        adj1 = random.choice(adjs)
        adj2 = random.choice(adjs)
        a1 = random.choice(neg_forms)
        a2 = random.choice(neg_forms)
        t = random.choice(templates)
        text = t.format(a1=a1, adj1=adj1, a2=a2, adj2=adj2).strip()
        if text.lower() in seen:
            continue
        seen.add(text.lower())
        prompts.append((text, "NEUTRAL"))

# Write to file
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
out_file = os.path.join(ROOT, 'test_100_mixed_prompts.txt')
with open(out_file, "w", encoding="utf-8") as f:
    for text, label in prompts:
        f.write(f"{text}\t{label}\n")

print(f"Wrote {len(prompts)} prompts to {out_file}")
