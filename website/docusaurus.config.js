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
        navbar: {
            hideOnScroll: true,
            style: 'dark',
            title: 'Ion Landscape',
            items: [
                {
                    href: '/ionlandscape/groups',
                    label: 'Groups',
                    position: 'right',
                },
                {
                    href: 'https://github.com/JovanMarkov96/ionlandscape',
                    label: 'GitHub',
                    position: 'right',
                },
            ],
        },
        colorMode: {
            defaultMode: 'light',
            disableSwitch: true,
        },
    },

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
