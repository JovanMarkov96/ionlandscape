const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

    // Connect to the local dev server instead of build
    await page.goto('http://localhost:3000/ionlandscape/', { waitUntil: 'networkidle0' });
    
    // Wait 5 seconds
    await new Promise(r => setTimeout(r, 5000));
    
    const mapHTML = await page.evaluate(() => {
        const el = document.querySelector('.map-viewport');
        return el ? el.innerHTML.substring(0, 500) : 'NO MAP VIEWPORT';
    });
    
    console.log('Map Viewport HTML start:', mapHTML);

    await page.screenshot({ path: 'map_debug.png' });
    await browser.close();
})();
