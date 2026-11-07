const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const V = '/home/claude/vendor/node_modules/';
const MAP = {
  'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js': V + 'gsap/dist/gsap.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js': V + 'gsap/dist/ScrollTrigger.min.js',
  'https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js': V + 'lenis/dist/lenis.min.js',
};
const W = 405, H = 720, DPR = 1080 / 405;
async function open(opts = {}) {
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--disable-lcd-text'] });
  const ctx = await browser.newContext({
    viewport: { width: W, height: H }, deviceScaleFactor: opts.dpr || DPR, isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',
    locale: 'ar-IQ', colorScheme: 'light', reducedMotion: 'no-preference',
  });
  await ctx.route(/^https?:\/\//, async r => {
    const u = r.request().url();
    if (MAP[u]) return r.fulfill({ status: 200, contentType: 'application/javascript', body: fs.readFileSync(MAP[u]) });
    return r.fulfill({ status: 404, body: '' });
  });
  await ctx.addInitScript({ path: path.join(__dirname, 'vclock.js') });
  const page = await ctx.newPage();
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto('file:///home/claude/shwani-media/docs/index.html', { waitUntil: 'load' });
  // make every picture decode now, not when it scrolls in
  await page.evaluate(async () => { const ims = [...document.images]; ims.forEach(i => i.loading = 'eager'); await Promise.all(ims.map(i => i.decode().catch(() => {}))); });
  // the hero picture fades into the page with a mask on the picture itself: the shade drawn over it left a 1px dark line at its top edge
  await page.addStyleTag({ content: '#hero .img img{-webkit-mask-image:linear-gradient(to bottom,transparent 0,rgba(0,0,0,.05) 9%,rgba(0,0,0,.22) 20%,rgba(0,0,0,.55) 32%,rgba(0,0,0,.85) 40%,#000 46%);mask-image:linear-gradient(to bottom,transparent 0,rgba(0,0,0,.05) 9%,rgba(0,0,0,.22) 20%,rgba(0,0,0,.55) 32%,rgba(0,0,0,.85) 40%,#000 46%)}#hero .img::before{display:none}' });
  const step = (ms) => page.evaluate(ms => window.__vt.step(ms), ms);
  return { browser, ctx, page, step, errs };
}
module.exports = { open, W, H, DPR };
