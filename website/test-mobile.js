// Mobile Responsive Test Script
// Run with: node test-mobile.js

const puppeteer = require('puppeteer');

const MOBILE_VIEWPORT = { width: 375, height: 667 }; // iPhone SE
const TABLET_VIEWPORT = { width: 768, height: 1024 }; // iPad
const DESKTOP_VIEWPORT = { width: 1280, height: 800 };

// Helper function to delay (replaces deprecated waitForTimeout)
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function testMobileResponsive() {
    console.log('🚀 Starting Mobile Responsive Tests...\n');

    const browser = await puppeteer.launch({
        headless: false, // Set to true for CI
        args: ['--no-sandbox']
    });

    const page = await browser.newPage();

    try {
        // Test 1: Desktop Layout
        console.log('📱 Test 1: Desktop Layout (1280x800)');
        await page.setViewport(DESKTOP_VIEWPORT);
        await page.goto('http://localhost:3000/ionlandscape/', { waitUntil: 'networkidle0', timeout: 30000 });
        await page.waitForSelector('.leaflet-container', { timeout: 10000 });

        const desktopPanel = await page.$('.ion-landscape-panel');
        const desktopPanelStyle = await page.evaluate(el => {
            const style = window.getComputedStyle(el);
            return {
                width: style.width,
                transform: style.transform,
                position: style.position
            };
        }, desktopPanel);

        console.log('  ✅ Desktop panel width:', desktopPanelStyle.width);
        console.log('  ✅ Desktop panel position:', desktopPanelStyle.position);
        await page.screenshot({ path: 'test-desktop.png', fullPage: false });
        console.log('  📸 Screenshot saved: test-desktop.png\n');

        // Test 2: Mobile Layout
        console.log('📱 Test 2: Mobile Layout (375x667)');
        await page.setViewport(MOBILE_VIEWPORT);
        await delay(500); // Wait for CSS transition

        const mobileToggle = await page.$('.mobile-panel-toggle');
        const toggleVisible = await page.evaluate(el => {
            const style = window.getComputedStyle(el);
            return style.display !== 'none';
        }, mobileToggle);

        console.log('  ✅ Mobile toggle button visible:', toggleVisible);

        const mobilePanelHidden = await page.evaluate(() => {
            const panel = document.querySelector('.ion-landscape-panel');
            const style = window.getComputedStyle(panel);
            return style.transform.includes('100') || !panel.classList.contains('panel-open');
        });
        console.log('  ✅ Panel initially hidden on mobile:', mobilePanelHidden);

        await page.screenshot({ path: 'test-mobile-initial.png', fullPage: false });
        console.log('  📸 Screenshot saved: test-mobile-initial.png\n');

        // Test 3: Open Panel on Mobile
        console.log('📱 Test 3: Open Panel via Toggle Button');
        await mobileToggle.click();
        await delay(400); // Wait for slide animation

        const panelOpen = await page.evaluate(() => {
            const panel = document.querySelector('.ion-landscape-panel');
            return panel.classList.contains('panel-open');
        });
        console.log('  ✅ Panel opened after clicking toggle:', panelOpen);

        await page.screenshot({ path: 'test-mobile-panel-open.png', fullPage: false });
        console.log('  📸 Screenshot saved: test-mobile-panel-open.png\n');

        // Test 4: Back to Map Button
        console.log('📱 Test 4: Back to Map Button');
        const backButton = await page.$('.back-to-map-btn');
        const backButtonVisible = await page.evaluate(el => {
            const style = window.getComputedStyle(el);
            return style.display !== 'none';
        }, backButton);
        console.log('  ✅ Back to Map button visible:', backButtonVisible);

        await backButton.click();
        await delay(400);

        const panelClosed = await page.evaluate(() => {
            const panel = document.querySelector('.ion-landscape-panel');
            return !panel.classList.contains('panel-open');
        });
        console.log('  ✅ Panel closed after Back to Map:', panelClosed);

        await page.screenshot({ path: 'test-mobile-panel-closed.png', fullPage: false });
        console.log('  📸 Screenshot saved: test-mobile-panel-closed.png\n');

        // Test 5: Click Map Marker
        console.log('📱 Test 5: Click Map Marker and Open Profile');
        const marker = await page.$('.leaflet-marker-icon');
        if (marker) {
            await marker.click();
            await delay(500);

            const popup = await page.$('.leaflet-popup');
            console.log('  ✅ Popup appeared:', !!popup);

            await page.screenshot({ path: 'test-mobile-popup.png', fullPage: false });

            // Click "Open profile" button
            const openProfileBtn = await page.$('.leaflet-popup-content button');
            if (openProfileBtn) {
                await openProfileBtn.click();
                await delay(500);

                const panelAutoOpened = await page.evaluate(() => {
                    const panel = document.querySelector('.ion-landscape-panel');
                    return panel.classList.contains('panel-open');
                });
                console.log('  ✅ Panel auto-opened after profile click:', panelAutoOpened);

                await page.screenshot({ path: 'test-mobile-profile.png', fullPage: false });
                console.log('  📸 Screenshot saved: test-mobile-profile.png\n');
            }
        } else {
            console.log('  ⚠️ No markers found on map (data may still be loading)\n');
        }

        // Test 6: Tablet Layout
        console.log('📱 Test 6: Tablet Layout (768x1024)');
        await page.setViewport(TABLET_VIEWPORT);
        await delay(500);

        const tabletPanelStyle = await page.evaluate(() => {
            const panel = document.querySelector('.ion-landscape-panel');
            const style = window.getComputedStyle(panel);
            return { width: style.width };
        });
        console.log('  ✅ Tablet panel width:', tabletPanelStyle.width);

        await page.screenshot({ path: 'test-tablet.png', fullPage: false });
        console.log('  📸 Screenshot saved: test-tablet.png\n');

        // Test 7: Groups Page & Filters
        console.log('📱 Test 7: Groups Page & Filters');
        await page.goto('http://localhost:3000/ionlandscape/groups', { waitUntil: 'networkidle0', timeout: 30000 });

        // Check scrolling (body overflow) - expecting 'auto'
        const groupsBodyOverflow = await page.evaluate(() => {
            return window.getComputedStyle(document.body).overflow;
        });
        console.log('  ✅ Groups Body Overflow:', groupsBodyOverflow);

        const filterBar = await page.$('.filter-bar');
        console.log('  ✅ Filter Bar present:', !!filterBar);

        if (filterBar) {
            // Try to select an option if available
            const firstSelect = await page.$('.filter-select');
            if (firstSelect) {
                // Determine a value to select? Hard without running app to see data.
                // We'll just verify the elements are there
                console.log('  ✅ Filter dropdowns present');
            }

            await page.screenshot({ path: 'test-groups-filters.png', fullPage: false });
            console.log('  📸 Screenshot saved: test-groups-filters.png\n');
        }

        // Test 8: Close Button on Desktop
        console.log('🖥️ Test 8: Close Button on Desktop');
        await page.setViewport(DESKTOP_VIEWPORT);
        await page.goto('http://localhost:3000/ionlandscape/', { waitUntil: 'networkidle0', timeout: 30000 });
        await page.waitForSelector('.leaflet-container', { timeout: 10000 });

        // Click a marker to open profile
        const markerDesktop = await page.$('.leaflet-marker-icon');
        if (markerDesktop) {
            await markerDesktop.click();
            await delay(500);

            // Look for "Open profile" button in popup
            const popupBtn = await page.$('.leaflet-popup-content button');
            if (popupBtn) {
                await popupBtn.click();
                await delay(1000);

                // Check if close button exists in panel
                const closeBtn = await page.$('.close-panel-btn');
                console.log('  ✅ Close button found:', !!closeBtn);

                if (closeBtn) {
                    // Click it
                    await closeBtn.click();
                    await delay(2000);

                    // Check if person is deselected (e.g. text "Click a marker" appears in panel)
                    const panelText = await page.evaluate(() => {
                        const p = document.querySelector('.ion-landscape-panel');
                        return p ? p.innerText : '';
                    });

                    const isCleared = panelText.includes('Click a marker') || panelText.includes('Ion Landscape');
                    console.log('  ✅ Panel verified cleared/closed:', isCleared);

                    if (!isCleared) {
                        console.log('     ❌ FAILED text content check. Got start of text: ', panelText.substring(0, 50).replace(/\n/g, ' '));
                    }
                } else {
                    console.log('  ⚠️ Close button NOT found (Profile might not have loaded or CSS issue)');
                }
            } else {
                console.log('  ⚠️ "Open profile" button not found in popup');
            }
        } else {
            console.log('  ⚠️ No markers found for Desktop test');
        }

        console.log('🎉 All tests completed!\n');
        console.log('Screenshots saved in the website directory.');

    } catch (error) {
        console.error('❌ Test failed:', error.message);
        await page.screenshot({ path: 'test-error.png', fullPage: false });
    } finally {
        await browser.close();
    }
}

testMobileResponsive().catch(console.error);
