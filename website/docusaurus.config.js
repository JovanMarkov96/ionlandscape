// website/docusaurus.config.js
module.exports = {
    title: 'Ion Landscape',
    tagline: 'Interactive map and academic family tree for trapped-ion & neutral-atom quantum computing',
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
    ],

    themeConfig: {
        // Disable the navbar for map-focused experience
        // Disable the navbar for map-focused experience
        navbar: {
            hideOnScroll: true,
            style: 'dark',
            items: [
                {
                    type: 'html',
                    position: 'left',
                    value: '<a href="/ionlandscape/" class="navbar-custom-btn" title="Home" aria-label="Home"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg><span class="navbar-btn-label">Home</span></a>',
                },
                {
                    type: 'html',
                    position: 'left', // Keep navigation on left/center usually, but user had right. Let's stick to user's "right" preference or standard. 'left' is better for main nav.
                    value: '<div style="flex-grow: 1;"></div>' // Spacer if needed, but let's just use position: right for the rest
                },
                {
                    type: 'html',
                    position: 'right',
                    value: '<a href="/ionlandscape/groups" class="navbar-custom-btn" title="Search" aria-label="Search"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg><span class="navbar-btn-label">Search</span></a>',
                },
                {
                    type: 'html',
                    position: 'right',
                    value: '<a href="https://github.com/JovanMarkov96/ionlandscape" target="_blank" rel="noopener noreferrer" class="navbar-custom-btn" title="GitHub" aria-label="GitHub"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg><span class="navbar-btn-label">GitHub</span></a>',
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
            copyright: `© ${new Date().getFullYear()} Ion Landscape | Developed by <a href="https://jovanmarkov96.github.io" target="_blank" rel="noopener noreferrer" style="color: var(--ifm-color-primary-lightest); font-weight: bold;">Jovan Markov</a>. Open Source Initiative.`,
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
