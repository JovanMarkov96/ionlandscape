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
