with open('dist/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

def parse_css_blocks(css):
    blocks = []
    i = 0
    n = len(css)
    while i < n:
        if css[i:i+6] == '@media':
            start = i
            brace = css.find('{', start)
            header = css[start:brace].strip()
            depth = 1
            j = brace + 1
            while j < n and depth > 0:
                if css[j] == '{':
                    depth += 1
                elif css[j] == '}':
                    depth -= 1
                j += 1
            body = css[brace+1:j-1]
            blocks.append((header, body))
            i = j
        else:
            i += 1
    return blocks

mq_blocks = parse_css_blocks(css)
print(f"Total media query blocks: {len(mq_blocks)}")
for header, body in mq_blocks:
    print(f"Header: {header} | Size: {len(body)} chars ({len(body)/1024:.1f} KB)")
