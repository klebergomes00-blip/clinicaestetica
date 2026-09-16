import re

with open('assets/00229412573a4838_styles-N9V2HjBQ.css', 'r', encoding='utf-8') as f:
    c1 = f.read()
with open('dist/styles.css', 'r', encoding='utf-8') as f:
    c2 = f.read()
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all class names from index.html
classes = set()
for m in re.finditer(r'class=["\']([^"\']+)["\']', html):
    for cls in m.group(1).split():
        classes.add(cls.strip())

print(f"Total unique classes in index.html: {len(classes)}")

style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
html_style = '\n'.join(style_blocks)

missing_in_c2 = []
found_in_c1_only = []

for cls in sorted(classes):
    escaped = re.escape(cls)
    in_c2 = bool(re.search(r'\.' + escaped + r'[\s{,.:>]', c2))
    in_style = bool(re.search(r'\.' + escaped + r'[\s{,.:>]', html_style))
    in_c1 = bool(re.search(r'\.' + escaped + r'[\s{,.:>]', c1))
    
    if not in_c2 and not in_style:
        missing_in_c2.append(cls)
        if in_c1:
            found_in_c1_only.append(cls)

print(f"Classes not in dist/styles.css or <style>: {len(missing_in_c2)}")
print(f"Of those, found in assets CSS: {len(found_in_c1_only)}")
print("Sample missing:", missing_in_c2[:40])
print("Found in assets CSS only:", found_in_c1_only[:40])
