import { spawn } from 'node:child_process';

async function test() {
  const p = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new', '--remote-debugging-port=9223', 'about:blank'
  ]);
  await new Promise(r => setTimeout(r, 1500));
  const res = await fetch('http://127.0.0.1:9223/json/new', { method: 'PUT' });
  const t = await res.json();
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  let id = 1; const cbs = new Map();
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && cbs.has(m.id)) { cbs.get(m.id)(m); cbs.delete(m.id); } };
  const send = (method, params = {}) => new Promise(r => { const i = id++; cbs.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  await send('Page.enable');
  await send('Runtime.enable');
  await send('Page.navigate', { url: 'http://localhost:8080/index.html' });
  await new Promise(r => setTimeout(r, 1500));
  const r = await send('Runtime.evaluate', {
    expression: `(() => {
      const allEls = Array.from(document.querySelectorAll('*'));
      allEls.unshift(document.body, document.documentElement);
      const findings = [];
      allEls.forEach(e => {
        if (!e) return;
        const s = window.getComputedStyle(e);
        const before = window.getComputedStyle(e, '::before');
        const after = window.getComputedStyle(e, '::after');
        
        [s, before, after].forEach((style, idx) => {
          const type = idx === 0 ? 'elem' : (idx === 1 ? '::before' : '::after');
          const checks = [
            style.borderTopColor, style.borderColor, style.outlineColor, style.backgroundColor, style.boxShadow
          ];
          const hasBlue = checks.some(c => c && (c.includes('rgb(0,') || c.includes('blue') || c.includes('rgba(0,') || c.includes('rgb(30,') || c.includes('rgb(59,')));
          const topBorder = parseFloat(style.borderTopWidth || '0') > 0;
          const outline = parseFloat(style.outlineWidth || '0') > 0;
          if (hasBlue || (topBorder && style.borderTopColor !== 'rgba(0, 0, 0, 0)') || outline) {
            findings.push({
              tag: e.tagName,
              id: e.id,
              cls: typeof e.className === 'string' ? e.className.slice(0, 50) : '',
              type,
              borderTop: style.borderTop,
              borderTopColor: style.borderTopColor,
              outline: style.outline,
              boxShadow: style.boxShadow
            });
          }
        });
      });
      return findings;
    })()`,
    returnByValue: true
  });
  console.log('DOM Findings:', JSON.stringify(r.result.result.value, null, 2));
  ws.close();
  p.kill();
}
test().catch(console.error);
