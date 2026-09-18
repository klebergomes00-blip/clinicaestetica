import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'<(h[1-6]|blockquote|cite|span|p|a|button)[^>]*class=[\'"]([^\'"]+)[\'"][^>]*>(.*?)(?=</\1>|(?=<[a-z]))', re.DOTALL | re.IGNORECASE)

matches = pattern.findall(html)
print(f"Total matching elements: {len(matches)}")

by_weight = {300: [], 400: [], 500: [], 600: [], 700: []}

for tag, cls, content in matches:
    cl = cls.split()
    clean = ' '.join(re.sub(r'<[^>]+>', ' ', content).split())[:40]
    if not clean:
        continue
    
    # Check font family
    is_heading = 'font-heading' in cl or 'hero-title' in cl
    is_mono = 'font-mono' in cl
    is_body = 'font-body' in cl or (not is_heading and not is_mono)
    
    # Weight
    w = 400
    if 'font-light' in cl:
        w = 300
    elif 'font-medium' in cl:
        w = 500
    elif 'font-semibold' in cl:
        w = 600
    elif 'font-bold' in cl:
        w = 700
        
    style = 'italic' if 'italic' in cl and 'not-italic' not in cl else 'normal'
    
    fam = 'Cormorant' if is_heading else ('JetBrains' if is_mono else 'Montserrat')
    by_weight[w].append((fam, tag, style, clean))

print("\n--- SUMMARY OF USAGE BY WEIGHT AND FAMILY ---")
for w in [300, 400, 500, 600, 700]:
    fams = {}
    for fam, tag, st, clean in by_weight[w]:
        key = f"{fam} ({st})"
        fams[key] = fams.get(key, 0) + 1
    print(f"Weight {w}: {fams}")
