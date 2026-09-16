import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<[^>]+class=["\'][^"\']*(?:font-heading|hero-title)[^"\']*["\'][^>]*>', html)
print(f"Total elements with font-heading or hero-title: {len(matches)}")
weights_found = set()
for m in matches:
    weights = [c for c in re.findall(r'font-(?:light|normal|medium|semibold|bold|extrabold)', m)]
    weights_found.update(weights)
    print(m[:100], "->", weights)

print("\nDistinct weights found on heading elements:", weights_found)
