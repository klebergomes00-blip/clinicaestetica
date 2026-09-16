import re
from collections import defaultdict

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find header
header = re.search(r'<header.*?</header>', html, re.DOTALL).group(0)
# Find heroSection
hero = re.search(r'<section id="heroSection".*?</section>', html, re.DOTALL).group(0)

print("=== ABOVE THE FOLD (Header & Hero) ===")

def analyze_html_block(name, block):
    print(f"\n--- {name} ---")
    classes = re.findall(r'class=["\']([^"\']+)["\']', block)
    all_classes = set()
    for c in classes:
        all_classes.update(c.split())
    font_weights = [c for c in all_classes if c in ['font-light', 'font-normal', 'font-medium', 'font-semibold', 'font-bold', 'font-extrabold']]
    font_families = [c for c in all_classes if c in ['font-heading', 'font-body', 'font-mono']]
    styles = [c for c in all_classes if c in ['italic', 'not-italic']]
    print("Font Families:", font_families)
    print("Font Weights:", font_weights)
    print("Font Styles:", styles)
    
    # Specific elements with typography
    elements = re.findall(r'<([a-zA-Z0-9]+)[^>]*class=["\']([^"\']+)["\'][^>]*>(.*?)</\1>', block, re.DOTALL)
    for tag, cls, content in elements:
        cl_list = cls.split()
        is_typo = any('font-' in c or c in ['italic'] for c in cl_list)
        if is_typo:
            clean = re.sub(r'<[^>]+>', '', content).strip()
            if clean:
                typo_classes = [c for c in cl_list if 'font-' in c or c in ['italic', 'text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl', 'text-3xl', 'text-4xl', 'text-5xl', 'text-6xl', 'text-7xl']]
                print(f"  [{tag}] ({' '.join(typo_classes)}): {clean[:70]}")

analyze_html_block("HEADER", header)
analyze_html_block("HERO SECTION", hero)

# Now check the rest of the page
rest_of_page = html[html.find('</section>')+10:]
analyze_html_block("BELOW THE FOLD (All other sections)", rest_of_page)
