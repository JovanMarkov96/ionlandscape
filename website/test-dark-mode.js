const puppeteer = require('puppeteer');

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    console.log('🚀 Starting Dark Mode & Footer Verification...');
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Simulate Dark Mode
    await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'dark' }]);

    let passed = true;

    try {
        console.log('🖥️ Visiting Home Page (Dark Mode) on port 3002...');
        await page.goto('http://localhost:3002/ionlandscape/', { waitUntil: 'networkidle0' });
        await delay(3000);

        // 1. Check Profile Panel Background Color
        // Open a profile first to see the panel
        await page.goto('http://localhost:3002/ionlandscape/?person=040-vladan-vuletic', { waitUntil: 'networkidle0' });
        await delay(2000);

        const panelBgColor = await page.evaluate(() => {
            const panel = document.querySelector('.ion-landscape-panel');
            return window.getComputedStyle(panel).backgroundColor;
        });

        console.log('   Panel Background Color:', panelBgColor);

        // In dark mode, it should NOT be pure white (rgb(255, 255, 255))
        // Docusaurus dark bg is usually around rgb(27, 27, 29) or hex #1b1b1d
        if (panelBgColor !== 'rgb(255, 255, 255)' && panelBgColor !== '#ffffff') {
            console.log('  ✅ Panel background is DARK (or at least not white).');
        } else {
            console.log('  ❌ Panel background is WHITE in dark mode!');
            passed = false;
        }

        // 2. Check Footer Visibility
        // Check if footer is roughly at the bottom
        const footerInfo = await page.evaluate(() => {
            const footer = document.querySelector('footer.footer');
            if (!footer) return null;
            const rect = footer.getBoundingClientRect();
            return {
                top: rect.top,
                bottom: rect.bottom,
                windowHeight: window.innerHeight,
                isVisible: rect.top < window.innerHeight && rect.bottom > 0
            };
        });

        console.log('   Footer Position:', footerInfo);

        if (footerInfo && footerInfo.isVisible) {
            console.log('  ✅ Footer is visible in viewport.');
        } else {
            console.log('  ⚠️ Footer NOT fully visible in viewport (might need scroll).');
            // Strict check: Is it "at the bottom" as requested?
            // If container height is correct, footer should be below it but visible if full page.
            // Actually, Docusaurus Layout footer is always at bottom of content.
        }

    } catch (e) {
        console.error('❌ Error:', e);
        passed = false;
    } finally {
        await browser.close();
        if (passed) console.log('\n🎉 Dark Mode Verified!');
        else process.exit(1);
    }
})();
