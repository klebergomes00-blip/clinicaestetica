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

def css_escape(s):
    # CSS selector escaping for tailwind classes
    # e.g., bg-caramel/15 -> bg-caramel\/15
    # -translate-x-1/2 -> \-translate-x-1\/2
    out = []
    for i, ch in enumerate(s):
        if ch in r'/:.[]%#()@,':
            out.append('\\' + ch)
        elif ch == '-' and i == 0:
            out.append(r'\-')
        else:
            out.append(ch)
    return ''.join(out)

style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
html_style = '\n'.join(style_blocks)

missing_in_c2 = []
found_in_c1 = []

for cls in sorted(classes):
    esc = css_escape(cls)
    # Check if selector like .esc exists
    pattern = re.escape('.' + esc) # wait, in raw string esc has literal \
    # In c2, the selector literally contains \/ for /
    # So we search for literal string '.' + esc
    in_c2 = ('.' + esc) in c2
    in_style = ('.' + cls) in html_style or ('.' + esc) in html_style
    in_c1 = ('.' + esc) in c1

    if not in_c2 and not in_style:
        missing_in_c2.append(cls)
        if in_c1:
            found_in_c1.append(cls)

print(f"Classes not in dist/styles.css or <style>: {len(missing_in_c2)}")
print(f"Of those, found in assets CSS: {len(found_in_c1)}")
if missing_in_c2:
    print("Sample missing:", missing_in_c2[:30])
if found_in_c1:
    print("Sample found in assets CSS:", found_in_c1[:30])
