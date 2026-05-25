// Render-verify the list pages with Puppeteer.
// Usage: node verify_pages.js <baseUrl>
const puppeteer = require('puppeteer');

const BASE = process.argv[2] || 'http://localhost:3030/ionlandscape';
const OUT = require('path').join(__dirname, '..', '..', '.logotest');
const fs = require('fs');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

async function checkPage(page, path, cardSelector) {
  const url = `${BASE}${path}`;
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
  // wait for cards to render
  await page.waitForSelector(cardSelector, { timeout: 30000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 1500));

  const data = await page.evaluate((sel) => {
    const cards = Array.from(document.querySelectorAll(sel));
    const result = {
      count: cards.length,
      heights: [],
      logoCount: 0,
      brokenImgs: 0,
      badgeCounts: [],
      headingPresent: !!document.querySelector('.institutions-header, .companies-header, .groups-header'),
    };
    cards.slice(0, 12).forEach(c => {
      result.heights.push(Math.round(c.getBoundingClientRect().height));
      const img = c.querySelector('img.inst-logo-img');
      if (img) {
        result.logoCount++;
        if (!img.complete || img.naturalWidth === 0) result.brokenImgs++;
      }
      result.badgeCounts.push(c.querySelectorAll('.badge').length);
    });
    return result;
  }, cardSelector);

  return { url, ...data };
}

(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 1000 });

  const pages = [
    ['/institutions', '.inst-card', 'institutions'],
    ['/companies', '.inst-card', 'companies'],
    ['/groups', '.inst-card', 'groups'],
  ];

  for (const [path, sel, name] of pages) {
    try {
      const r = await checkPage(page, path, sel);
      console.log(`\n=== ${name} (${r.url}) ===`);
      console.log(`  cards: ${r.count}`);
      console.log(`  logos rendered: ${r.logoCount}, broken: ${r.brokenImgs}`);
      console.log(`  heading still present: ${r.headingPresent}`);
      console.log(`  first-row heights: ${r.heights.slice(0,3).join(', ')}`);
      console.log(`  badge counts (first 6): ${r.badgeCounts.slice(0,6).join(', ')}`);
      await page.goto(`${BASE}${path}`, { waitUntil: 'networkidle2' });
      await new Promise(res => setTimeout(res, 1500));
      await page.screenshot({ path: `${OUT}/verify-${name}.png`, fullPage: false });
      console.log(`  screenshot: .logotest/verify-${name}.png`);
    } catch (e) {
      console.log(`\n=== ${name} FAILED: ${e.message}`);
    }
  }

  await browser.close();
})();
