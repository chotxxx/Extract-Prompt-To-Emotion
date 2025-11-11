from collections import Counter
from pathlib import Path
import re

p = Path('failed_patterns.txt')
if not p.exists():
    print('failed_patterns.txt not found')
    raise SystemExit(1)

lines = [l.strip() for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]

# Parse lines: format: TEXT\tGT:LABEL\tFusion:LABEL\tPhoBERT:LABEL\tRule:LABEL
entries = []
for ln in lines:
    parts = ln.split('\t')
    text = parts[0]
    gt = None
    for part in parts[1:]:
        if part.startswith('GT:'):
            gt = part[3:]
    entries.append((text, gt))

# Tokenize simple: lower, split on non-word, keep 1-3 grams
def tokenize(s):
    s = s.lower()
    toks = [t for t in re.split(r"\W+", s) if t]
    return toks

unigrams = Counter()
bigrams = Counter()
trigrams = Counter()
label_counts = Counter()
neg_examples = []
for text, gt in entries:
    toks = tokenize(text)
    label_counts[gt] += 1
    for i in range(len(toks)):
        unigrams[toks[i]] += 1
        if i+1 < len(toks):
            bigrams[' '.join(toks[i:i+2])] += 1
        if i+2 < len(toks):
            trigrams[' '.join(toks[i:i+3])] += 1
    if gt == 'NEGATIVE':
        neg_examples.append(text)

print('Total failed entries:', len(entries))
print('Label counts among failures:', dict(label_counts))
print('\nTop unigrams:')
for w,c in unigrams.most_common(30):
    print(f'{w}: {c}')
print('\nTop bigrams:')
for w,c in bigrams.most_common(30):
    print(f'{w}: {c}')
print('\nTop trigrams:')
for w,c in trigrams.most_common(30):
    print(f'{w}: {c}')

# Show top negative examples for quick inspection
print('\nSample NEGATIVE failure examples:')
for t in neg_examples[:30]:
    print('-', t)

# Produce a conservative candidate list: bigrams/trigrams that appear >=2 and look negative by containing known negative words
known_neg = set(['te','tệ','xau','xấu','khong','không','toi','tồi','toi te','khủng','khung','khiep','thất','that','khong'])
candidates = []
for phrase, cnt in trigrams.most_common(200):
    if cnt >= 2 and any(k in phrase for k in known_neg):
        candidates.append((phrase, cnt))
for phrase, cnt in bigrams.most_common(200):
    if cnt >= 3 and any(k in phrase for k in known_neg):
        candidates.append((phrase, cnt))

print('\nSuggested candidate phrases (conservative):')
for ph,c in candidates[:40]:
    print(ph, c)

# write suggestions to file
out = Path('scripts/failure_analysis_suggestions.txt')
with out.open('w', encoding='utf-8') as f:
    f.write('Total failed entries: %d\n' % len(entries))
    f.write('Label counts: %s\n\n' % dict(label_counts))
    f.write('Top unigrams:\n')
    for w,c in unigrams.most_common(50):
        f.write(f'{w}: {c}\n')
    f.write('\nTop bigrams:\n')
    for w,c in bigrams.most_common(50):
        f.write(f'{w}: {c}\n')
    f.write('\nSuggested candidate phrases (conservative):\n')
    for ph,c in candidates[:100]:
        f.write(f'{ph}\t{c}\n')

print('\nWrote suggestions to scripts/failure_analysis_suggestions.txt')
