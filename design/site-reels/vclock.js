// Virtual clock: makes JS + CSS animation time deterministic so every frame can be captured at leisure.
(() => {
  let now = 0;
  const D0 = 1762531200000; // fixed epoch
  let rafQ = [], rafId = 0, tid = 1;
  const timers = new Map();
  performance.now = () => now;
  Date.now = () => D0 + now;
  window.requestAnimationFrame = cb => { const id = ++rafId; rafQ.push([id, cb]); return id; };
  window.cancelAnimationFrame = id => { rafQ = rafQ.filter(x => x[0] !== id); };
  window.setTimeout = (fn, ms, ...a) => { const id = tid++; timers.set(id, { at: now + Math.max(0, +ms || 0), fn, a }); return id; };
  window.clearTimeout = id => { timers.delete(id); };
  window.setInterval = (fn, ms, ...a) => { const id = tid++; const ev = Math.max(4, +ms || 0); timers.set(id, { at: now + ev, fn, a, ev }); return id; };
  window.clearInterval = id => { timers.delete(id); };
  const run = f => { try { f(); } catch (e) { console.error('vclock', e && e.stack || e); } };
  window.__vt = {
    get now() { return now; },
    step(dt) {
      const target = now + dt;
      for (let guard = 0; guard < 500; guard++) {
        let best = null;
        for (const [id, t] of timers) if (t.at <= target && (!best || t.at < best[1].at)) best = [id, t];
        if (!best) break;
        const [id, t] = best; now = Math.max(now, t.at);
        if (t.ev) t.at += t.ev; else timers.delete(id);
        run(() => typeof t.fn === 'function' ? t.fn(...t.a) : (0, eval)(t.fn));
      }
      now = target;
      const q = rafQ; rafQ = [];
      for (const [, cb] of q) run(() => cb(now));
      for (const an of document.getAnimations()) {
        if (an.__vs === undefined) { an.__vs = now - dt; an.pause(); }
        an.currentTime = now - an.__vs;
      }
      return now;
    }
  };
})();
