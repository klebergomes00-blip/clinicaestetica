import re
from pathlib import Path

content = Path('index.html').read_text(encoding='utf-8')
css1 = Path('assets/00229412573a4838_styles-N9V2HjBQ.css').read_text(encoding='utf-8', errors='ignore')
css2 = Path('assets/99c4515b30a30010_css2.css').read_text(encoding='utf-8', errors='ignore')

all_content = content + '\n' + css1 + '\n' + css2

print("=== CHECKING ASSETS FOLDER ===")
for f in sorted(Path('assets').glob('*')):
    if f.is_file():
        name = f.name
        # check if filename is in all_content
        found = name in all_content
        print(f"{'[USED]' if found else '[UNUSED]'} assets/{name} ({f.stat().st_size // 1024} KB)")

print("\n=== CHECKING MEDIA FOLDER ===")
for f in sorted(Path('media').glob('*')):
    if f.is_file():
        name = f.name
        # also check url-encoded name
        name_enc = name.replace(' ', '%20')
        found = (name in all_content) or (name_enc in all_content)
        print(f"{'[USED]' if found else '[UNUSED]'} media/{name} ({f.stat().st_size // 1024} KB)")
