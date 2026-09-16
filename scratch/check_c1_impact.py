import re

with open('assets/00229412573a4838_styles-N9V2HjBQ.css', 'r', encoding='utf-8') as f:
    c1 = f.read()
with open('dist/styles.css', 'r', encoding='utf-8') as f:
    c2 = f.read()
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's see what selectors or rules in c1 might be affecting index.html
# First, let's extract all words / tags / ids / classes from index.html
ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
tags = set(re.findall(r'<([a-zA-Z0-9]+)', html))
classes = set()
for m in re.finditer(r'class=["\']([^"\']+)["\']', html):
    for cls in m.group(1).split():
        classes.add(cls.strip())

print(f"Index.html has {len(tags)} tags, {len(ids)} ids, {len(classes)} classes")

# Does c1 have any rule for any id in index.html?
matching_ids = [id_name for id_name in ids if f"#{id_name}" in c1]
print(f"IDs in c1: {matching_ids}")

# Are there any custom animations or keyframes in c1?
c1_keyframes = re.findall(r'@keyframes\s+([a-zA-Z0-9_-]+)', c1)
print(f"Keyframes in c1: {c1_keyframes}")
c2_keyframes = re.findall(r'@keyframes\s+([a-zA-Z0-9_-]+)', c2)
print(f"Keyframes in c2: {c2_keyframes}")

# Any font-face in c1?
c1_fonts = re.findall(r'@font-face\s*{([^}]+)}', c1)
print(f"Font faces in c1: {len(c1_fonts)}")
