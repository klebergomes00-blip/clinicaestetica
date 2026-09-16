with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="heroSection"')
end = text.find('</section>', start)
hero_html = text[start:end]

for line in hero_html.splitlines():
    line_s = line.strip()
    if any(k in line_s for k in ['<h1', '<h2', '<p', '<span', '<a', '<button', 'class=']) and any(k in line_s for k in ['font', 'text-', 'hero-', 'tracking-']):
        print(line_s[:140])
