import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Split page into Above the fold (up to end of heroSection) and Below the fold
hero_end_idx = html.find('</section>') # First </section> is heroSection
above_fold = html[:hero_end_idx + 10]
below_fold = html[hero_end_idx + 10:]

def find_weights_and_elements(chunk, section_name):
    print(f"\n==================== {section_name} ====================")
    # Find all elements with classes
    pattern = re.compile(r'<([a-z0-9]+)\s+[^>]*class=["\']([^"\']+)["\'][^>]*>(.*?)(?:</\1>|(?=<[a-z0-9]))', re.DOTALL | re.IGNORECASE)
    weight_usage = {
        '300 (font-light)': [],
        '400 (normal/default)': [],
        '500 (font-medium)': [],
        '600 (font-semibold)': [],
        '700 (font-bold)': [],
    }
    
    for tag, cls, content in pattern.findall(chunk):
        cl_list = cls.split()
        clean_text = re.sub(r'<[^>]+>', ' ', content).strip()
        # Clean extra whitespace
        clean_text = ' '.join(clean_text.split())
        if not clean_text or len(clean_text) < 2:
            continue
            
        # Is it heading font or mono font?
        is_heading = 'font-heading' in cl_list or 'hero-title' in cl_list
        is_mono = 'font-mono' in cl_list
        
        # Determine weight
        w = None
        if 'font-light' in cl_list:
            w = '300 (font-light)'
        elif 'font-medium' in cl_list:
            w = '500 (font-medium)'
        elif 'font-semibold' in cl_list:
            w = '600 (font-semibold)'
        elif 'font-bold' in cl_list:
            w = '700 (font-bold)'
        elif not is_heading and not is_mono:
            # Default body weight is 400 (normal)
            w = '400 (normal/default)'
            
        if w:
            weight_usage[w].append((tag, cls, clean_text[:60], is_heading, is_mono))
            
    for weight, items in weight_usage.items():
        print(f"\n--- Weight {weight} (Total: {len(items)}) ---")
        for item in items[:5]:
            print(f"  [{item[0]}] {item[2]} (classes: {item[1][:40]}...)")

find_weights_and_elements(above_fold, "ABOVE THE FOLD (Header & Hero)")
find_weights_and_elements(below_fold, "BELOW THE FOLD (Rest of Page)")
