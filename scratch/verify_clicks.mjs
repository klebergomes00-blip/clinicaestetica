import { spawn } from 'node:child_process';

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const cp = spawn(chromePath, [
  '--headless=new',
  '--remote-debugging-port=9225',
  '--disable-gpu',
  '--no-first-run',
  'http://localhost:3000/index.html'
]);

setTimeout(async () => {
  try {
    const list = await (await fetch('http://127.0.0.1:9225/json')).json();
    const pageTarget = list.find(t => t.type === 'page') || list[0];
    const wsUrl = pageTarget.webSocketDebuggerUrl;
    const ws = new WebSocket(wsUrl);
    await new Promise(r => ws.onopen = r);

    let id = 1;
    function send(method, params = {}) {
      return new Promise(r => {
        const msgId = id++;
        const handler = (e) => {
          const m = JSON.parse(e.data);
          if (m.id === msgId) {
            ws.removeEventListener('message', handler);
            r(m);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: msgId, method, params }));
      });
    }

    await send('Page.enable');
    await send('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });
    await send('Page.navigate', { url: 'http://localhost:3000/index.html' });
    await new Promise(r => setTimeout(r, 2500));
    await send('Runtime.enable');
    const res = await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = document.querySelector('.beam-btn');
        if (!btn) {
          return { error: 'btn not found', href: location.href, title: document.title, bodyLength: document.body ? document.body.innerHTML.length : 0 };
        }
        const r = btn.getBoundingClientRect();
        btn.scrollIntoView({ block: 'center' });
        const r2 = btn.getBoundingClientRect();
        const el = document.elementFromPoint(r2.x + r2.width / 2, r2.y + r2.height / 2);
        
        let clicked = false;
        btn.addEventListener('click', (e) => { clicked = true; });
        el.click();

        return {
          rect: { x: r2.x, y: r2.y, width: r2.width, height: r2.height },
          elTag: el ? el.tagName : null,
          elClass: el ? el.className : null,
          isInside: btn.contains(el),
          clickedFired: clicked
        };
      })()`,
      returnByValue: true
    });
    console.log('CLICK TARGET TEST:', JSON.stringify(res));
    ws.close();
  } catch(e) {
    console.error(e);
  } finally {
    cp.kill();
  }
}, 2500);
