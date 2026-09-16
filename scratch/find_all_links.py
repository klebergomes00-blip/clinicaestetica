import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== ALL LINKS & BUTTONS IN INDEX.HTML ===")
for i, line in enumerate(lines, start=1):
    links = re.findall(r'<a\s+[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', line, re.DOTALL)
    if not links:
        # Check multiline <a>
        pass
    for href, text in links:
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        print(f"Line {i:4d}: href='{href}' | text='{clean_text[:50]}'")

# Multiline check
full_html = "".join(lines)
for m in re.finditer(r'<a\s+([^>]*?)>(.*?)</a>', full_html, re.DOTALL):
    attrs = m.group(1)
    text = m.group(2)
    href_m = re.search(r'href=["\']([^"\']*)["\']', attrs)
    href = href_m.group(1) if href_m else 'NO_HREF'
    clean_text = re.sub(r'<[^>]+>', ' ', text).strip()
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    # Calculate line number
    line_no = full_html[:m.start()].count('\n') + 1
    print(f"Line {line_no:4d}: href='{href}' | text='{clean_text[:60]}'")
