import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

p1 = '<link rel="preconnect" href="https://fonts.googleapis.com">' in html
p2 = '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' in html
print(f"Preconnect fonts.googleapis.com: {p1}")
print(f"Preconnect fonts.gstatic.com: {p2}")

gf_match = re.search(r'<link[^>]*fonts\.googleapis\.com/css2\?([^"\'>]+)[^>]*>', html)
if gf_match:
    print("Google Fonts URL params:", gf_match.group(1))

legacy_css2 = '99c4515b30a30010_css2.css' in html
print(f"Legacy duplicate CSS2 stylesheet removed from index.html: {not legacy_css2}")
