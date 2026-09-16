import urllib.request
import re
import os

os.makedirs('assets/fonts', exist_ok=True)

url = 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
with urllib.request.urlopen(req) as resp:
    css = resp.read().decode('utf-8')

blocks = re.findall(r'/\* ([^*]+) \*/\s*@font-face\s*{([^}]+)}', css)
print(f"Total font blocks found: {len(blocks)}")

# Subsets for pt-BR: latin and latin-ext
target_subsets = {'latin', 'latin-ext'}

local_font_faces = []
downloaded = 0

for subset_raw, block in blocks:
    subset = subset_raw.strip()
    if subset not in target_subsets:
        continue
    
    m_fam = re.search(r"font-family:\s*['\"]?([^'\";]+)['\"]?;", block)
    m_weight = re.search(r"font-weight:\s*(\d+);", block)
    m_style = re.search(r"font-style:\s*(\w+);", block)
    m_src = re.search(r"src:\s*url\((https://[^)]+)\)\s*format\(['\"]?woff2['\"]?\);", block)
    m_range = re.search(r"unicode-range:\s*([^;]+);", block)
    
    if not (m_fam and m_weight and m_style and m_src):
        continue
        
    family = m_fam.group(1).strip()
    weight = m_weight.group(1).strip()
    style = m_style.group(1).strip()
    font_url = m_src.group(1).strip()
    unicode_range = m_range.group(1).strip() if m_range else None
    
    # Safe filename
    fam_slug = family.lower().replace(' ', '-')
    filename = f"{fam_slug}-{style}-{weight}-{subset}.woff2"
    filepath = os.path.join('assets/fonts', filename)
    
    if not os.path.exists(filepath):
        print(f"Downloading {filename} from {font_url}...")
        u_req = urllib.request.Request(font_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(u_req) as u_resp, open(filepath, 'wb') as out_f:
            out_f.write(u_resp.read())
        downloaded += 1
    
    rule = f"""@font-face {{
  font-family: '{family}';
  font-style: {style};
  font-weight: {weight};
  font-display: swap;
  src: url('assets/fonts/{filename}') format('woff2');"""
    if unicode_range:
        rule += f"\n  unicode-range: {unicode_range};"
    rule += "\n}"
    local_font_faces.append(rule)

print(f"Downloaded {downloaded} font files. Generated {len(local_font_faces)} @font-face rules.")

with open('scratch/local_fonts.css', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(local_font_faces))
