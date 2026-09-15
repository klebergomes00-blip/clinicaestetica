import re
from pathlib import Path

content = Path('index.html').read_text(encoding='utf-8')
urls = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', content)
css_urls = re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', content)

all_refs = sorted(set(urls + css_urls))
local_refs = []
external_refs = []

for r in all_refs:
    if r.startswith(('http://', 'https://', 'data:', 'mailto:', 'tel:')):
        external_refs.append(r)
    elif r.startswith('#'):
        continue
    else:
        local_refs.append(r)

print("=== LOCAL ASSETS REFERENCED IN index.html ===")
for r in local_refs:
    p = Path(r)
    exists = p.exists()
    print(f"[{'EXISTS' if exists else 'MISSING'}] {r}")

print("\n=== EXTERNAL REFS ===")
for r in external_refs:
    print(f"  {r}")
