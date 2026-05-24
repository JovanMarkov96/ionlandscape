const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const ROOT = path.resolve(__dirname, '..', '..');
const LOGO_DIR = path.join(ROOT, 'website', 'static', 'img', 'institutions');

async function svgToPng(svgPath, outPath) {
  const svg = fs.readFileSync(svgPath, 'utf8');
  const svgB64 = Buffer.from(svg).toString('base64');
  const html = `<!doctype html><html><meta charset="utf-8"><body style="margin:0;background:transparent"><div id="wrap" style="width:256px;height:256px;display:flex;align-items:center;justify-content:center;background:transparent"><img src="data:image/svg+xml;base64,${svgB64}" style="max-width:100%;max-height:100%;"/></div></body></html>`;

  const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox','--disable-setuid-sandbox']});
  const page = await browser.newPage();
  await page.setViewport({width:256, height:256});
  await page.setContent(html, {waitUntil: 'networkidle0'});
  const el = await page.$('#wrap');
  await el.screenshot({path: outPath, omitBackground: true});
  await browser.close();
}

async function main() {
  const files = fs.readdirSync(LOGO_DIR).filter(f => f.endsWith('.svg'));
  for (const f of files) {
    const id = path.basename(f, '.svg');
    const svgPath = path.join(LOGO_DIR, f);
    const outPath = path.join(LOGO_DIR, `${id}_mark.png`);
    try {
      await svgToPng(svgPath, outPath);
      console.log('converted', f, '->', path.basename(outPath));
    } catch (e) {
      console.error('failed', f, e);
    }
  }
}

main().catch(e=>{console.error(e);process.exit(1)});
