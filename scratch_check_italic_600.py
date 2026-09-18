import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'<([a-zA-Z0-9]+)[^>]*class=[\'"]([^\'"]+)[\'"][^>]*>(.*?)(?=</\1>|(?=<[a-z]))', re.DOTALL | re.IGNORECASE)
matches = pattern.findall(html)

print("Elements with BOTH italic and (semibold or 600 or bold):")
for tag, cls, content in matches:
    cl = cls.split()
    if ('italic' in cl or 'font-style: italic' in cls) and ('font-semibold' in cl or '600' in cl or 'font-bold' in cl or '700' in cl):
        clean = ' '.join(re.sub(r'<[^>]+>', ' ', content).split())[:60]
        print(f"<{tag} class='{cls}'>: {clean}")

# Also check <b> or <strong> containing italic
strong_italic = re.findall(r'<(?:strong|b)[^>]*>.*?(?:italic|font-heading).*?</(?:strong|b)>', html, re.DOTALL)
print("\nStrong/b containing italic/heading:", strong_italic)
