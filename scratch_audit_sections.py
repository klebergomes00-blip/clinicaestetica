import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find all sections
section_pattern = re.compile(r'(<section[^>]*>|<header[^>]*>|<footer[^>]*>)(.*?)(?=<(?:section|header|footer)|$)', re.DOTALL)
sections = section_pattern.findall(html)
print(f"Total sections/header/footer: {len(sections)}")

# We want to map:
# font-heading: Cormorant Garamond (or Athelas fallback)
# font-body: Montserrat
# font-mono: JetBrains Mono

# Also check explicit classes:
# font-light -> 300
# font-normal -> 400
# font-medium -> 500
# font-semibold -> 600
# font-bold -> 700
# italic -> style: italic

for tag, content in sections:
    sec_id = re.search(r'id=[\'"]([^\'"]+)', tag)
    sec_aria = re.search(r'aria-label=[\'"]([^\'"]+)', tag)
    tag_name = re.search(r'<([a-zA-Z0-9]+)', tag).group(1)
    name = sec_id.group(1) if sec_id else (sec_aria.group(1) if sec_aria else tag_name)
    
    print(f"\n=======================================================")
    print(f"SECTION: <{tag_name}> ID: {name}")
    print(f"=======================================================")
    
    # Find all elements with classes
    elements = re.findall(r'<([a-zA-Z0-9]+)\s+[^>]*class=[\'"]([^\'"]+)[\'"][^>]*>(.*?)(?=</\1>|(?=<[a-zA-Z0-9]))', content, re.DOTALL)
    
    usage_by_family = {
        'Cormorant Garamond (font-heading / hero-title)': [],
        'Montserrat (font-body / default)': [],
        'JetBrains Mono (font-mono)': []
    }
    
    for el_tag, cls, text in elements:
        cl_list = cls.split()
        clean = re.sub(r'<[^>]+>', ' ', text).strip()
        clean = ' '.join(clean.split())
        if not clean or len(clean) < 2:
            continue
            
        # Determine family
        fam = None
        if 'font-mono' in cl_list:
            fam = 'JetBrains Mono (font-mono)'
        elif 'font-heading' in cl_list or 'hero-title' in cl_list or 'hero-title-line-1' in cl_list or 'hero-title-line-2' in cl_list:
            fam = 'Cormorant Garamond (font-heading / hero-title)'
        else:
            fam = 'Montserrat (font-body / default)'
            
        # Determine weight
        w = 400
        if 'font-light' in cl_list:
            w = 300
        elif 'font-medium' in cl_list:
            w = 500
        elif 'font-semibold' in cl_list:
            w = 600
        elif 'font-bold' in cl_list:
            w = 700
            
        # Determine style
        style = 'italic' if 'italic' in cl_list and 'not-italic' not in cl_list else 'normal'
        
        usage_by_family[fam].append((el_tag, w, style, clean[:50], cls[:40]))
        
    for fam, items in usage_by_family.items():
        if items:
            weights = sorted(list(set((w, st) for _, w, st, _, _ in items)))
            print(f"  [{fam}] Weights & Styles: {weights}")
            for it in items[:4]:
                print(f"    <{it[0]}> (weight {it[1]}, {it[2]}): \"{it[3]}\"")
