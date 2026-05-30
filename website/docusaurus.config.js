// website/docusaurus.config.js
module.exports = {
    title: 'Quantum Landscape',
    tagline: 'Interactive map and academic family tree of the quantum technology landscape — platforms, people, institutions & companies',
    url: 'https://JovanMarkov96.github.io',
    baseUrl: '/ionlandscape/',
    onBrokenLinks: 'warn',
    onBrokenMarkdownLinks: 'warn',
    favicon: 'img/favicon.ico',
    organizationName: 'JovanMarkov96',
    projectName: 'ionlandscape',

    // Head tags for mobile optimization
    headTags: [
        {
            tagName: 'meta',
            attributes: {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no',
            },
        },
        {
            tagName: 'meta',
            attributes: {
                name: 'apple-mobile-web-app-capable',
                content: 'yes',
            },
        },
        {
            tagName: 'meta',
            attributes: {
                name: 'mobile-web-app-capable',
                content: 'yes',
            },
        },
        {
            tagName: 'link',
            attributes: {
                rel: 'apple-touch-icon',
                href: '/ionlandscape/img/apple-touch-icon.png',
            },
        },
        {
            tagName: 'meta',
            attributes: {
                name: 'theme-color',
                content: '#020B1C',
            },
        },
    ],

    themeConfig: {
        image: 'img/brand/social-card.png',
        // Disable the navbar for map-focused experience
        // Disable the navbar for map-focused experience
        navbar: {
            hideOnScroll: true,
            style: 'dark',
            items: [
                {
                    type: 'html',
                    position: 'left',
                    value: '<a href="/ionlandscape/" class="ql-brand" title="Quantum Landscape — Home" aria-label="Quantum Landscape Home"><img class="ql-brand-img ql-wordmark ql-wordmark-dark" src="/ionlandscape/img/brand/wordmark-horizontal-on-dark.png" alt="Quantum Landscape" /><img class="ql-brand-img ql-wordmark ql-wordmark-light" src="/ionlandscape/img/brand/wordmark-horizontal-on-light.png" alt="Quantum Landscape" /><img class="ql-brand-img ql-mark-only" src="/ionlandscape/img/brand/mark.png" alt="Quantum Landscape" /></a>',
                },
                {
                    type: 'html',
                    position: 'right',
                    value: '<a href="/ionlandscape/groups" class="navbar-custom-btn" title="People" aria-label="People"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg><span class="navbar-btn-label">People</span></a>',
                },
                {
                    type: 'html',
                    position: 'right',
                    value: '<a href="/ionlandscape/companies" class="navbar-custom-btn" title="Companies" aria-label="Companies"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><path d="M9 22v-4h6v4"></path><path d="M8 6h.01"></path><path d="M16 6h.01"></path><path d="M12 6h.01"></path><path d="M12 10h.01"></path><path d="M12 14h.01"></path><path d="M16 10h.01"></path><path d="M16 14h.01"></path><path d="M8 10h.01"></path><path d="M8 14h.01"></path></svg><span class="navbar-btn-label">Companies</span></a>',
                },
                {
                    type: 'html',
                    position: 'right',
                    value: '<a href="/ionlandscape/institutions" class="navbar-custom-btn" title="Institutions" aria-label="Institutions"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="22" x2="21" y2="22"></line><line x1="6" y1="18" x2="6" y2="11"></line><line x1="10" y1="18" x2="10" y2="11"></line><line x1="14" y1="18" x2="14" y2="11"></line><line x1="18" y1="18" x2="18" y2="11"></line><polygon points="12 2 20 7 4 7"></polygon></svg><span class="navbar-btn-label">Institutions</span></a>',
                },
                {
                    type: 'html',
                    position: 'right',
                    value: '<a href="/ionlandscape/lineages" class="navbar-custom-btn" title="Graph" aria-label="Graph"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg><span class="navbar-btn-label">Graph</span></a>',
                },
                {
                    type: 'html',
                    position: 'right',
                    value: '<a href="https://github.com/JovanMarkov96/ionlandscape" target="_blank" rel="noopener noreferrer" class="navbar-custom-btn" title="GitHub" aria-label="GitHub"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg><span class="navbar-btn-label">GitHub</span></a>',
                },
                {
                    type: 'html',
                    position: 'right',
                    value: '<a href="https://ko-fi.com/quantum_landscape" target="_blank" rel="noopener noreferrer" class="navbar-custom-btn navbar-support-btn" title="Support Quantum Landscape — an independent open-source project" aria-label="Support this project"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg><span class="navbar-btn-label">Support</span></a>',
                },
                {
                    type: 'html',
                    position: 'right',
                    value: '<button class="navbar-custom-btn share-nav-btn" onclick="openSharePopup()" title="Share" aria-label="Share"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg><span class="navbar-btn-label">Share</span></button>',
                },
            ],
        },
        colorMode: {
            defaultMode: 'light',
            disableSwitch: false,
            respectPrefersColorScheme: true,
        },
        footer: {
            style: 'dark',
            links: [],
            copyright: `© ${new Date().getFullYear()} Quantum Landscape | Developed by <a href="https://jovanmarkov96.github.io" target="_blank" rel="noopener noreferrer" style="color: var(--ifm-color-primary-lightest); font-weight: bold;">Jovan Markov</a>. Open Source Initiative.`,
        },
    },

    scripts: [
        {
            src: '/ionlandscape/js/share.js',
            async: true,
        },
    ],

    presets: [
        [
            '@docusaurus/preset-classic',
            {
                docs: false,
                blog: false,
                theme: {
                    customCss: require.resolve('./src/css/custom.css'),
                },
            },
        ],
    ],
};
