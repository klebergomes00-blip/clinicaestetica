import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Above the fold is from <body to id="filosofia"
above_fold = html[html.find('<body'):html.find('id="filosofia"')]
below_fold = html[html.find('id="filosofia"'):]

print("=== ABOVE THE FOLD (Header & Hero) ===")

# Search for all elements with class in above_fold
classes_above = set()
for m in re.finditer(r'class=["\']([^"\']+)["\']', above_fold):
    for c in m.group(1).split():
        classes_above.add(c)

print("Font family classes above fold:", [c for c in classes_above if 'font-' in c])
print("Font weights above fold:", [c for c in classes_above if c.startswith('font-') and c in ['font-light', 'font-normal', 'font-medium', 'font-semibold', 'font-bold']])
print("Italic above fold:", 'italic' in classes_above)

# Let's inspect text elements in header and hero
print("\nHeader & Hero text inspection:")
for m in re.finditer(r'<([a-zA-Z0-9]+)[^>]*class=["\']([^"\']+)["\'][^>]*>(.*?)</\1>', above_fold, re.DOTALL):
    tag, cls, text = m.group(1), m.group(2), m.group(3).strip()
    if text and not text.startswith('<') and len(text) < 100:
        if any(w in cls for w in ['font-', 'italic', 'text-', 'hero-title', 'nav-link', 'beam-btn']):
            print(f"  <{tag} class='{cls}'>: {text[:60]}")

print("\n=== BELOW THE FOLD ===")
classes_below = set()
for m in re.finditer(r'class=["\']([^"\']+)["\']', below_fold):
    for c in m.group(1).split():
        classes_below.add(c)

print("Font weights below fold:", [c for c in classes_below if c.startswith('font-') and c in ['font-light', 'font-normal', 'font-medium', 'font-semibold', 'font-bold']])
print("Font family classes below fold:", [c for c in classes_below if 'font-' in c])
