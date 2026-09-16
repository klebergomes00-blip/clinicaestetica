with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

chars_outside_latin1 = set()
for ch in text:
    cp = ord(ch)
    # Check if outside U+0000-00FF and common punctuation U+2000-206F / U+2190-21FF
    if cp > 0x00FF:
        chars_outside_latin1.add((ch, f"U+{cp:04X}"))

print("Characters outside U+0000-00FF in index.html:")
for ch, hexcode in sorted(chars_outside_latin1, key=lambda x: x[1]):
    print(f"  {ch} ({hexcode})")
