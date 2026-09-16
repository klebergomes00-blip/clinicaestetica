import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('=== LCP AUDIT CHECKLIST ===')
print('1. Preload Mobile in <head>:', 'media/video-preview-thumb-mobile.webp' in html)
print('2. Preload Desktop in <head>:', 'media/video-preview-thumb.webp' in html)

m_video = re.search(r'<video\s+id="heroMobileVideo"[\s\S]*?</video>', html)
if m_video:
    vc = m_video.group(0)
    print('3. heroMobileVideo poster is WebP:', 'poster="media/video-preview-thumb-mobile.webp"' in vc)
    print('4. heroMobileVideo img has fetchpriority="high":', 'fetchpriority="high"' in vc)
    print('5. heroMobileVideo img has loading="eager":', 'loading="eager"' in vc)
    print('6. heroMobileVideo img does NOT have loading="lazy":', 'loading="lazy"' not in vc)
    print('7. heroMobileVideo img has width & height:', 'width="720"' in vc and 'height="1280"' in vc)
else:
    print('ERROR: heroMobileVideo not found!')

d_video = re.search(r'<div class="parallax-layer parallax-layer-2"[\s\S]*?</video>', html)
if d_video:
    dc = d_video.group(0)
    print('8. Desktop video poster is WebP:', 'poster="media/video-preview-thumb.webp"' in dc)
    print('9. Desktop img has fetchpriority="high":', 'fetchpriority="high"' in dc)
    print('10. Desktop img has loading="eager":', 'loading="eager"' in dc)

print('=== ASSET SIZES ===')
for p in ['media/video-preview-thumb-mobile.webp', 'media/video-preview-thumb.webp', 'media/video-preview-thumb-15s.webp']:
    if os.path.exists(p):
        print(f'{p}: {os.path.getsize(p)} bytes ({os.path.getsize(p)/1024:.1f} KB)')
    else:
        print(f'{p}: NOT FOUND')
