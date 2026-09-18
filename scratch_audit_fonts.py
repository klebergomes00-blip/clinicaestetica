import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check preloads
preloads = re.findall(r'<link[^>]*rel=[\'"]preload[\'"][^>]*as=[\'"]font[\'"][^>]*>', html)
print('--- PRELOADS IN INDEX.HTML ---')
for p in preloads:
    print(p)

# Check imports in all css/html
imports = re.findall(r'@import[^;]+;', html)
print('\n--- IMPORTS IN INDEX.HTML ---')
for imp in imports:
    print(imp)

# Check all @font-face in index.html
font_faces = re.findall(r'@font-face\s*\{[^}]+\}', html)
print(f'\n--- @FONT-FACE DECLARATIONS IN INDEX.HTML (Total: {len(font_faces)}) ---')
for ff in font_faces:
    family = re.search(r'font-family:\s*[\'"]?([^\'";]+)', ff)
    weight = re.search(r'font-weight:\s*([^\'";]+)', ff)
    style = re.search(r'font-style:\s*([^\'";]+)', ff)
    src = re.search(r'src:\s*url\([\'"]?([^\'")]+)', ff)
    display = re.search(r'font-display:\s*([^\'";]+)', ff)
    ur = re.search(r'unicode-range:\s*([^\'";]+)', ff)
    fam_s = family.group(1).strip() if family else '?'
    w_s = weight.group(1).strip() if weight else 'normal'
    st_s = style.group(1).strip() if style else 'normal'
    src_s = src.group(1).strip() if src else '?'
    disp_s = display.group(1).strip() if display else 'NONE'
    ur_s = 'Latin-ext' if 'U+0100' in (ur.group(1) if ur else '') else 'Latin'
    print(f'Family: {fam_s:20} | Weight: {w_s:6} | Style: {st_s:6} | Display: {disp_s:6} | Range: {ur_s:9} | Src: {src_s}')

# Check dist/styles.css as well
try:
    with open('dist/styles.css', 'r', encoding='utf-8') as f:
        css = f.read()
    ff_css = re.findall(r'@font-face\s*\{[^}]+\}', css)
    print(f'\n--- @FONT-FACE DECLARATIONS IN DIST/STYLES.CSS (Total: {len(ff_css)}) ---')
    for ff in ff_css:
        print(ff[:120])
    imp_css = re.findall(r'@import[^;]+;', css)
    print(f'Imports in dist/styles.css: {imp_css}')
except Exception as e:
    print('dist/styles.css error:', e)
