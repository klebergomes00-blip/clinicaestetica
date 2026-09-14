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

  // Wait for Chrome to be ready
  await new Promise(r => setTimeout(r, 1500));

  try {
    const versionRes = await fetch('http://127.0.0.1:9222/json/new', { method: 'PUT' });
    const target = await versionRes.json();
    const wsUrl = target.webSocketDebuggerUrl;

    const ws = new WebSocket(wsUrl);
    await new Promise(resolve => ws.onopen = resolve);

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

    // Desktop 1440x900
    await send('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });

    await send('Page.navigate', { url: 'http://localhost:3000/index.html' });
    await new Promise(r => setTimeout(r, 2000));

    // Test 1: Button clickability and pointer-events
    const clickCheck = await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = document.querySelector('.beam-btn');
        const rect = btn.getBoundingClientRect();
        const elemAtPoint = document.elementFromPoint(rect.x + rect.width / 2, rect.y + rect.height / 2);
        const isInsideBtn = btn.contains(elemAtPoint);
        const fgLayer = document.getElementById('heroForegroundLayer');
        const fgPointerEvents = fgLayer ? getComputedStyle(fgLayer).pointerEvents : 'none';
        return { isInsideBtn, fgPointerEvents, clickedTag: elemAtPoint ? elemAtPoint.tagName : null };
      })()`,
      returnByValue: true
    });
    console.log('Clickability Test Result:', JSON.stringify(clickCheck.result.value));

    // Test 2: Pause video at 5 different time points across loop (2s, 8s, 15s, 22s, 28s)
    const timePoints = [2, 8, 15, 22, 28];
    const artifactDir = 'C:\\Users\\Kleber Gomes\\.gemini\\antigravity-ide\\brain\\5bd40295-8cab-4891-b009-d60a61fe0f6b';

    for (const t of timePoints) {
      console.log(`Pausing video at ${t}s to test contrast...`);
      await send('Runtime.evaluate', {
        expression: `(() => {
          const v = document.querySelector('.parallax-layer-2 video');
          if (v) {
            v.pause();
            v.currentTime = ${t};
          }
        })()`
      });
      await new Promise(r => setTimeout(r, 600));

      const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 85 });
      const outPath = resolve(artifactDir, `hero_loop_frame_${t}s.jpg`);
      writeFileSync(outPath, Buffer.from(shot.result.data, 'base64'));
      console.log(`Saved screenshot for ${t}s to: ${outPath}`);
    }

    // Test 3: Mobile at 390x844 with particles & overlay
    console.log('Testing Mobile 390x844 layout...');
    await send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 1200));
    const mobileShot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 85 });
    const mobilePath = resolve(artifactDir, 'hero_mobile_particles_qa.jpg');
    writeFileSync(mobilePath, Buffer.from(mobileShot.result.data, 'base64'));
    console.log(`Saved Mobile QA screenshot to: ${mobilePath}`);

    ws.close();
  } finally {
    chromeProc.kill();
  }
}

run().catch(console.error);
