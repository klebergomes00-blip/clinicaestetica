import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Search for JetBrains Mono / font-mono
mono_matches = []
for i, line in enumerate(html.splitlines(), 1):
    if 'JetBrains' in line or 'font-mono' in line or 'mono' in line.lower():
        mono_matches.append((i, line.strip()))

print(f"Total lines mentioning mono / JetBrains: {len(mono_matches)}")
for line_no, content in mono_matches[:30]:
    print(f"  Line {line_no}: {content[:100]}")

# 2. Check font weights used in HTML
# In Tailwind: font-light = 300, font-normal = 400, font-medium = 500, font-semibold = 600, font-bold = 700
weight_classes = ['font-light', 'font-normal', 'font-medium', 'font-semibold', 'font-bold']
weight_counts = {}
for w in weight_classes:
    weight_counts[w] = len(re.findall(r'\b' + w + r'\b', html))

print("\nFont weight classes in index.html:")
for w, cnt in weight_counts.items():
    print(f"  {w}: {cnt}")

# 3. Check what is above the fold (up to #heroSection or #filosofia)
hero_cutoff = html.find('id="filosofia"')
above_fold_html = html[:hero_cutoff]

above_weights = {}
for w in weight_classes:
    above_weights[w] = len(re.findall(r'\b' + w + r'\b', above_fold_html))

print("\nFont weight classes ABOVE the fold:")
for w, cnt in above_weights.items():
    print(f"  {w}: {cnt}")

# Check italic above fold
print(f"Italic above fold: {len(re.findall(r'italic', above_fold_html))}")

# Check Cormorant Garamond usage above fold vs whole page
print(f"font-heading above fold: {len(re.findall(r'font-heading|hero-title', above_fold_html))}")
