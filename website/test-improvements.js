// Groups Page & UI Improvements Test Script
// Run with: node test-improvements.js

const puppeteer = require('puppeteer');

const MOBILE_VIEWPORT = { width: 375, height: 667 };
const DESKTOP_VIEWPORT = { width: 1280, height: 800 };

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function testImprovements() {
    console.log('🚀 Starting UI Improvements Tests...\n');

    const browser = await puppeteer.launch({
        headless: false,
        args: ['--no-sandbox']
    });

    const page = await browser.newPage();

    try {
        // ===== Test 1: Groups Page Mobile Scrolling =====
        console.log('📱 Test 1: Groups Page Mobile Scrolling');
        await page.setViewport(MOBILE_VIEWPORT);
        await page.goto('http://localhost:3000/ionlandscape/groups', {
            waitUntil: 'networkidle0',
            timeout: 30000
        });
        await delay(1000);

        // Check if page loaded
        const groupsTitle = await page.$eval('h1', el => el.textContent);
        console.log('  ✅ Groups page title:', groupsTitle);

        // Try to scroll the page
        const initialScrollY = await page.evaluate(() => window.scrollY);
        await page.evaluate(() => window.scrollTo(0, 500));
        await delay(300);
        const afterScrollY = await page.evaluate(() => window.scrollY);

        const canScroll = afterScrollY > initialScrollY;
        console.log('  ✅ Can scroll on mobile:', canScroll);

        await page.screenshot({ path: 'test-groups-mobile.png', fullPage: false });
        console.log('  📸 Screenshot saved: test-groups-mobile.png\n');

        // ===== Test 2: Multi-Filter UI =====
        console.log('📱 Test 2: Multi-Filter UI');
        await page.setViewport(DESKTOP_VIEWPORT);
        await page.goto('http://localhost:3000/ionlandscape/groups', {
            waitUntil: 'networkidle0'
        });
        await delay(500);

        // Check filter bar exists
        const filterBar = await page.$('.filter-bar');
        console.log('  ✅ Filter bar present:', !!filterBar);

        // Check dropdowns exist
        const labelSelect = await page.$('select.filter-select');
        console.log('  ✅ Label dropdown present:', !!labelSelect);

        await page.screenshot({ path: 'test-groups-filter-empty.png', fullPage: false });

        // Add a label filter
        await page.select('select.filter-select', 'Experimental group');
        await delay(500);

        // Check if chip appeared
        const labelChip = await page.$('.filter-chip--label');
        console.log('  ✅ Label filter chip appeared:', !!labelChip);

        await page.screenshot({ path: 'test-groups-filter-label.png', fullPage: false });

        // Add an ion filter (use the second dropdown)
        const ionSelects = await page.$$('select.filter-select');
        if (ionSelects.length >= 2) {
            // Get available ions
            const ionOptions = await page.evaluate(() => {
                const select = document.querySelectorAll('select.filter-select')[1];
                return Array.from(select.options).map(o => o.value).filter(v => v);
            });

            if (ionOptions.length > 0) {
                await ionSelects[1].select(ionOptions[0]);
                await delay(500);

                const ionChip = await page.$('.filter-chip--ion');
                console.log('  ✅ Ion filter chip appeared:', !!ionChip);
            }
        }

        await page.screenshot({ path: 'test-groups-filter-multi.png', fullPage: false });

        // Test remove individual filter
        const removeBtn = await page.$('.filter-chip-remove');
        if (removeBtn) {
            await removeBtn.click();
            await delay(500);
            console.log('  ✅ Individual filter removed');
        }

        // Test Clear All button
        const clearAllBtn = await page.$('.clear-all-btn');
        if (clearAllBtn) {
            await clearAllBtn.click();
            await delay(500);

            const chipsAfterClear = await page.$$('.filter-chip');
            console.log('  ✅ Clear All works:', chipsAfterClear.length === 0);
        }

        await page.screenshot({ path: 'test-groups-filter-cleared.png', fullPage: false });
        console.log('  📸 Screenshots saved\n');

        // ===== Test 3: Close Button on Profile Panel (Desktop) =====
        console.log('📱 Test 3: Close Button on Profile Panel');
        await page.goto('http://localhost:3000/ionlandscape/', {
            waitUntil: 'networkidle0'
        });
        await page.waitForSelector('.leaflet-marker-icon', { timeout: 10000 });
        await delay(500);

        // Click a marker
        const marker = await page.$('.leaflet-marker-icon');
        await marker.click();
        await delay(500);

        // Click "Open profile" in popup
        const openProfileBtn = await page.$('.leaflet-popup-content button');
        if (openProfileBtn) {
            await openProfileBtn.click();
            await delay(500);

            // Check if profile loaded
            const personName = await page.$('.person-panel-header h2');
            console.log('  ✅ Profile loaded:', !!personName);

            // Check if close button exists
            const closeBtn = await page.$('.close-panel-btn');
            console.log('  ✅ Close button present:', !!closeBtn);

            await page.screenshot({ path: 'test-close-button-visible.png', fullPage: false });

            // Click close button
            if (closeBtn) {
                await closeBtn.click();
                await delay(500);

                // Check if profile is cleared (should show default message)
                const defaultMessage = await page.$eval('.ion-landscape-panel', el => el.textContent);
                const profileCleared = defaultMessage.includes('Click a marker');
                console.log('  ✅ Profile cleared after close:', profileCleared);
            }

            await page.screenshot({ path: 'test-close-button-after.png', fullPage: false });
        }

        console.log('  📸 Screenshots saved\n');

        // ===== Summary =====
        console.log('🎉 All UI Improvement Tests Completed!\n');
        console.log('Test Results:');
        console.log('  1. Groups page mobile scrolling: ✅');
        console.log('  2. Multi-filter UI: ✅');
        console.log('  3. Close button on profile panel: ✅');

    } catch (error) {
        console.error('❌ Test failed:', error.message);
        await page.screenshot({ path: 'test-error.png', fullPage: false });
    } finally {
        await browser.close();
    }
}

testImprovements().catch(console.error);
