with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'cormorant' in line.lower() and '600' in line.lower():
        print(f"Line {i+1}: {line.strip()[:100]}")
    if 'font-heading' in line and any(k in line for k in ['600', 'semibold', 'bold']):
        print(f"Heading with 600 line {i+1}: {line.strip()[:100]}")
