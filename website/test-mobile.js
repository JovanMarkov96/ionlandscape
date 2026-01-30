const puppeteer = require('puppeteer');

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    console.log('🚀 Starting Mobile Layout Verification...');
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    // Emulate iPhone SE
    await page.setViewport({ width: 375, height: 667, isMobile: true, hasTouch: true });

    let passed = true;

    try {
        console.log('📱 Visiting Home Page on port 3002...');
        await page.goto('http://localhost:3002/ionlandscape/', { waitUntil: 'networkidle0' });
        await delay(3000);

        // 1. Check Navbar (Should NOT have hamburger)
        const isHamburgerVisible = await page.evaluate(() => {
            const toggle = document.querySelector('.navbar__toggle');
            return toggle && window.getComputedStyle(toggle).display !== 'none';
        });

        console.log('   Hamburger Menu Disabled:', !isHamburgerVisible);
        if (!isHamburgerVisible) {
            console.log('  ✅ Hamburger menu is HIDDEN as requested.');
        } else {
            console.log('  ❌ Hamburger menu is STILL VISIBLE.');
            passed = false;
        }

        // 2. Check Navbar Items (Should be visible)
        const areItemsVisible = await page.evaluate(() => {
            const groupsLink = document.querySelector('a[href="/ionlandscape/groups"]');
            return groupsLink && window.getComputedStyle(groupsLink).display !== 'none';
        });

        if (areItemsVisible) {
            console.log('  ✅ Navbar items (Groups) are VISIBLE.');
        } else {
            console.log('  ❌ Navbar items are HIDDEN.');
            passed = false;
        }

        // 3. Check Panel Overlay Z-Index
        // Open a profile
        await page.goto('http://localhost:3002/ionlandscape/?person=040-vladan-vuletic', { waitUntil: 'networkidle0' });
        await delay(2000);

        const checkOverlay = await page.evaluate(() => {
            const panel = document.querySelector('.ion-landscape-panel');
            const zoomControl = document.querySelector('.leaflet-control-zoom');

            if (!panel || !zoomControl) return { error: 'Elements not found' };

            const panelZ = window.getComputedStyle(panel).zIndex;
            // Leaflet controls usually don't have explicit z-index on the element itself, 
            // but the container .leaflet-top has z-index 1000.
            // We just need panelZ > 1000.

            return { panelZ: parseInt(panelZ, 10) };
        });

        console.log('   Panel Z-Index:', checkOverlay.panelZ);
        if (checkOverlay.panelZ >= 2000) {
            console.log('  ✅ Panel Z-Index is high (2000+). Should cover map controls.');
        } else {
            console.log('  ❌ Panel Z-Index is too low:', checkOverlay.panelZ);
            passed = false;
        }

    } catch (e) {
        console.error('❌ Error:', e);
        passed = false;
    } finally {
        await browser.close();
        if (passed) console.log('\n🎉 Mobile Fixes Verified!');
        else process.exit(1);
    }
})();
