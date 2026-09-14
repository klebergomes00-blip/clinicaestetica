import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

async function run() {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const chromeProc = spawn(chromePath, [
    '--headless=new',
    '--remote-debugging-port=9222',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    'about:blank'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const versionRes = await fetch('http://127.0.0.1:9222/json/new', { method: 'PUT' });
    const target = await versionRes.json();
    const wsUrl = target.webSocketDebuggerUrl;

    const ws = new WebSocket(wsUrl);
    await new Promise(res => ws.onopen = res);

    let id = 1;
    const callbacks = new Map();

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg);
        callbacks.delete(msg.id);
      }
    };

    function send(method, params = {}) {
      return new Promise((resolve) => {
        const msgId = id++;
        callbacks.set(msgId, resolve);
        ws.send(JSON.stringify({ id: msgId, method, params }));
      });
    }

    await send('Page.enable');
    await send('Runtime.enable');
    await send('DOM.enable');

    await send('Page.navigate', { url: 'http://localhost:8080/index.html' });
    await new Promise(r => setTimeout(r, 2000));

    const breakpoints = [
      { w: 320, h: 568, name: '320px_se' },
      { w: 360, h: 640, name: '360px_android' },
      { w: 375, h: 667, name: '375px_iphone' },
      { w: 390, h: 844, name: '390px_iphone14' },
      { w: 414, h: 896, name: '414px_plus' },
      { w: 480, h: 800, name: '480px_large_mobile' },
      { w: 768, h: 1024, name: '768px_tablet' },
      { w: 980, h: 1200, name: '980px_tablet_large' },
      { w: 1024, h: 768, name: '1024px_desktop_sm' },
      { w: 1280, h: 800, name: '1280px_desktop_md' },
      { w: 1440, h: 900, name: '1440px_desktop_lg' },
      { w: 1920, h: 1080, name: '1920px_desktop_fhd' }
    ];

    const artifactDir = 'C:\\Users\\Kleber Gomes\\.gemini\\antigravity-ide\\brain\\9f3bc5ef-a0d0-4dbf-8a0a-99285827144f';
    const results = [];

    for (const bp of breakpoints) {
      const isMobile = bp.w < 1024;
      await send('Emulation.setDeviceMetricsOverride', {
        width: bp.w,
        height: bp.h,
        deviceScaleFactor: 1,
        mobile: isMobile
      });
      await new Promise(r => setTimeout(r, 400));

      const evalRes = await send('Runtime.evaluate', {
        expression: `(() => {
          try {
            const docEl = document.documentElement;
            const body = document.body;
            const scrollW = Math.max(docEl.scrollWidth || 0, body.scrollWidth || 0);
            const clientW = window.innerWidth;
            const hasHScroll = scrollW > clientW;

            const titleEl = document.querySelector('.hero-title');
            const titleRect = titleEl ? titleEl.getBoundingClientRect() : null;
            const btnEl = document.querySelector('.beam-btn');
            const btnRect = btnEl ? btnEl.getBoundingClientRect() : null;

            const isMobile = window.innerWidth < 1024;
            const activeVideo = isMobile
              ? document.getElementById('heroMobileVideo')
              : document.querySelector('.parallax-layer-2 video');

            return {
              w: clientW,
              scrollW: scrollW,
              hasHScroll: hasHScroll,
              overflowDiff: Math.max(0, scrollW - clientW),
              titleWidth: titleRect ? Math.round(titleRect.width) : 0,
              btnWidth: btnRect ? Math.round(btnRect.width) : 0,
              videoTag: activeVideo ? activeVideo.tagName : 'none'
            };
          } catch(e) {
            return { error: e.message };
          }
        })()`,
        returnByValue: true
      });

      const metrics = evalRes.result ? evalRes.result.value : { error: JSON.stringify(evalRes) };
      results.push({ bp: bp.name, ...metrics });

      // Capture screenshot for key verification sizes
      if ([320, 375, 390, 768, 1280, 1440].includes(bp.w)) {
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 88 });
        const outPath = resolve(artifactDir, `verify_${bp.name}.jpg`);
        writeFileSync(outPath, Buffer.from(shot.result.data, 'base64'));
      }
    }

    console.log(JSON.stringify(results, null, 2));

    ws.close();
  } finally {
    chromeProc.kill();
  }
}

run().catch(console.error);
