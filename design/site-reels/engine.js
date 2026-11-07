// Record the portfolio at phone size, frame by frame on a virtual clock, following a plan of timed actions.
// node engine.js plan.json outdir [--preview]   (preview: 1 frame of every 15, at css scale)
const { open } = require('./rig');
const fs = require('fs'), path = require('path');
const [planPath, outDir, flag] = process.argv.slice(2);
const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
const FPS = 30, PREVIEW = flag === '--preview';
const ease = { lin: t => t, io: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, out: t => 1 - Math.pow(1 - t, 3), sio: t => -(Math.cos(Math.PI * t) - 1) / 2 };

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const { browser, page, step, errs } = await open({ dpr: PREVIEW ? 1 : undefined });
  await page.evaluate(() => {
    const d = document.createElement('div'); d.id = '__tch';
    d.style.cssText = 'position:fixed;left:0;top:0;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;background:rgba(255,255,255,.6);box-shadow:0 0 0 1.5px rgba(32,33,38,.22),0 3px 12px rgba(32,33,38,.22);pointer-events:none;z-index:2147483647;opacity:0';
    document.body.appendChild(d);
    window.__tch = (x, y, o, s) => { d.style.opacity = o; d.style.transform = `translate(${x}px,${y}px) scale(${s})`; };
    const st = sel => ScrollTrigger.getAll().find(t => t.trigger && t.trigger.matches && t.trigger.matches(sel) && t.vars && t.vars.scrub && t.vars.onUpdate);
    window.__Y = (spec) => {
      if (typeof spec === 'number') return spec;
      const [sel, mode, v] = spec;               // ['#hw','p',0.5] progress of a pinned/scrubbed section, ['#facts','top',-20]
      if (mode === 'p') { const t = st(sel); if (t) return t.start + (t.end - t.start) * v; }
      if (mode === 'serv') { const t = ScrollTrigger.getAll().find(t => t.trigger && t.trigger.id === 'services' && !t.vars.scrub); return t.start + (t.end - t.start) * ((v + 0.5) / 7); }
      const el = document.querySelector(sel), r = el.getBoundingClientRect();
      if (mode === 'p') return r.top + scrollY + (r.height - innerHeight) * v;
      if (mode === 'max') return document.documentElement.scrollHeight - innerHeight;
      return r.top + scrollY + (v || 0);
    };
    const E = { io: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2, lin: t => t, out: t => 1 - Math.pow(1 - t, 3), sio: t => -(Math.cos(Math.PI * t) - 1) / 2 };
    window.__scroll = (spec, dur, e) => { const y = window.__Y(spec); window.__lenis.scrollTo(y, { duration: dur, easing: E[e || 'io'], force: true, lock: true }); return y; };
  });
  if (plan.start !== undefined) {           // open on a section, not on the front page
    for (let i = 0; i < 10; i++) await step(1000 / FPS);
    await page.evaluate(s => window.__lenis.scrollTo(window.__Y(s), { immediate: true, force: true }), plan.start);
    await step(1000 / FPS);
  }
  const acts = plan.actions.map(a => ({ ...a })).sort((a, b) => a.at - b.at);
  const N = Math.round(plan.dur * FPS);
  const log = [];
  let touch = null;            // {x,y,t0,t1,kind}
  const drags = [], pvs = [];
  const where = async (a) => {
    if (a.xy) return { x: a.xy[0], y: a.xy[1] };
    return page.evaluate(([sel, fx, fy]) => {
      let el;
      if (sel === 'center-piece') { const sh = document.querySelector('#shelf').getBoundingClientRect(); el = [...document.querySelectorAll('#shRow > .pz')].reduce((a, b) => { const c = e => Math.abs(e.getBoundingClientRect().x + e.getBoundingClientRect().width / 2 - sh.x - sh.width / 2); return c(b) < c(a) ? b : a; }); }
      else if (sel.startsWith('nth-hs:')) el = document.querySelectorAll('#pv .hs')[+sel.slice(7)];
      else el = document.querySelector(sel);
      const r = el.getBoundingClientRect(); return { x: r.x + r.width * (fx ?? .5), y: r.y + r.height * (fy ?? .5) };
    }, [a.el, a.fx, a.fy]);
  };
  let ai = 0;
  for (let f = 0; f < N; f++) {
    const t = f / FPS;
    while (ai < acts.length && acts[ai].at <= t + 1e-6) {
      const a = acts[ai++];
      if (a.type === 'scroll') { const y = await page.evaluate(([s, d, e]) => window.__scroll(s, d, e), [a.to, a.dur, a.ease]); log.push([t, 'scroll', JSON.stringify(a.to), Math.round(y)]); }
      else if (a.type === 'tap') { const p = await where(a); touch = { ...p, t0: t, t1: t + .45, kind: 'tap', fired: false }; log.push([t, 'tap', a.el || a.xy, Math.round(p.x), Math.round(p.y)]); }
      else if (a.type === 'drag') {
        const p0 = await where({ el: a.el, fx: a.from[0], fy: a.from[1] }), p1 = await where({ el: a.el, fx: a.to[0], fy: a.to[1] });
        drags.push({ p0, p1, t0: t, t1: t + a.dur, down: false }); log.push([t, 'drag', a.el]);
      }
      else if (a.type === 'pvscroll') { const s0 = await page.evaluate(() => document.querySelector('#pvSc').scrollTop); pvs.push({ s0, by: a.by, t0: t, t1: t + a.dur }); }
      else if (a.type === 'eval') await page.evaluate(a.js);
    }
    // touches
    let tx = -100, ty = -100, to = 0, ts = 1;
    if (touch) {
      const k = (t - touch.t0) / (touch.t1 - touch.t0);
      if (!touch.fired && t - touch.t0 >= .12) { await page.mouse.click(touch.x, touch.y); touch.fired = true; }
      if (k >= 1) touch = null; else { tx = touch.x; ty = touch.y; to = k < .25 ? k / .25 : 1 - (k - .25) / .75; ts = k < .25 ? 1.15 - .25 * (k / .25) : .9 + .2 * (k - .25); }
    }
    for (const d of drags) {
      if (t < d.t0 || d.done) continue;
      const k = Math.min(1, (t - d.t0) / (d.t1 - d.t0)), e = ease.io(k);
      const x = d.p0.x + (d.p1.x - d.p0.x) * e, y = d.p0.y + (d.p1.y - d.p0.y) * e;
      if (!d.down) { await page.mouse.move(d.p0.x, d.p0.y); await page.mouse.down(); d.down = true; }
      await page.mouse.move(x, y);
      tx = x; ty = y; to = Math.min(1, (t - d.t0) / .12); ts = .95;
      if (k >= 1) { await page.mouse.up(); d.done = true; d.tEnd = t; }
    }
    for (const d of drags) if (d.done && t - d.tEnd < .25) { tx = d.p1.x; ty = d.p1.y; to = 1 - (t - d.tEnd) / .25; ts = .95; }
    for (const p of pvs) { if (t < p.t0 || t > p.t1 + .05) continue; const k = Math.min(1, (t - p.t0) / (p.t1 - p.t0)); await page.evaluate(v => document.querySelector('#pvSc').scrollTop = v, p.s0 + p.by * ease.sio(k)); }
    await page.evaluate(([x, y, o, s]) => window.__tch(x, y, o, s), [tx, ty, Math.max(0, to).toFixed(3), ts.toFixed(3)]);
    await step(1000 / FPS);
    if (!PREVIEW || f % 15 === 0) await page.screenshot({ path: path.join(outDir, `f${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: PREVIEW ? 70 : 93 });
    if (f % 150 === 0) process.stdout.write(`${f}/${N} `);
  }
  fs.writeFileSync(path.join(outDir, 'log.json'), JSON.stringify({ log, errs }, null, 1));
  console.log('\nerrors', errs.slice(0, 5));
  await browser.close();
})();
