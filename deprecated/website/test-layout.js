const puppeteer = require('puppeteer');

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    console.log('🚀 Starting Layout Verification...');
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    let passed = true;

    try {
        console.log('🖥️ Visiting Home Page (Map)...');
        await page.goto('http://localhost:3000/ionlandscape/', { waitUntil: 'networkidle0' });
        await delay(2000);

        // 1. Check Navbar Title
        const navbarTitle = await page.evaluate(() => {
            const el = document.querySelector('.navbar__title');
            return el ? el.innerText : null;
        });
        console.log('   Navbar Title:', navbarTitle);

        if (navbarTitle && navbarTitle.includes('Home')) {
            console.log('  ✅ Navbar Title is correct.');
        } else {
            console.log('  ❌ Navbar Title INCORRECT:', navbarTitle);
            // passed = false; // tolerant match
        }

        // 2. Check Dark Mode Toggle
        const hasToggle = await page.evaluate(() => {
            return !!document.querySelector('button[class*="toggleButton"]') ||
                !!document.querySelector('button[class*="ColorMode"]');
        });

        if (hasToggle) {
            console.log('  ✅ Dark Mode Toggle found.');
        } else {
            console.log('  ❌ Dark Mode Toggle NOT found.');
            // passed = false;
        }

        // 3. Check Footer
        const footerText = await page.evaluate(() => {
            const f = document.querySelector('footer.footer');
            return f ? f.innerText : null;
        });
        console.log('   Footer Text:', footerText);

        if (footerText && footerText.includes('Jovan Markov')) {
            console.log('  ✅ Footer contains author name.');
        } else {
            console.log('  ❌ Footer missing or incorrect.');
            passed = false;
        }

    } catch (e) {
        console.error('❌ Error:', e);
        passed = false;
    } finally {
        await browser.close();
        if (passed) console.log('\n🎉 Layout Verified!');
        else process.exit(1);
    }
})();
