from PIL import Image
import os, io

p = 'media/video-preview-thumb-mobile.webp'
im = Image.open(p)
orig_sz = os.path.getsize(p)
print(f"Original: {im.size}, size: {orig_sz} bytes ({orig_sz/1024:.1f} KiB)")

for w, q in [(720, 78), (720, 75), (720, 72), (640, 78), (640, 75), (540, 78), (480, 80), (480, 75)]:
    h = int(w * im.size[1] / im.size[0])
    resized = im.resize((w, h), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    resized.save(buf, format='WEBP', quality=q, method=6)
    data = buf.getvalue()
    saving = (orig_sz - len(data)) / 1024
    print(f"Width={w}x{h}, q={q} -> {len(data)} bytes ({len(data)/1024:.1f} KiB), saving: {saving:.1f} KiB")
