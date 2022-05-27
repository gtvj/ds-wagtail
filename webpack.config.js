const path = require('path');

module.exports = {
    mode: 'production',
    entry: {
        beta_banner: './scripts/src/beta-banner.js',
        image_viewer: './scripts/src/image-viewer.js',
        home_page: './scripts/src/home-page.js',
        explorer: './scripts/src/explorer.js',
        insights: './scripts/src/insights.js',
        image_browse: './scripts/src/image-browse.js',
        details: './scripts/src/details.js',
        sign_in: './scripts/src/sign-in.js',
        global_search: './scripts/src/global-search.js',
        catalogue_search: './scripts/src/catalogue-search.js',
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'templates/static/scripts'),
    },
    module: {
        rules: [
            {
                test: /\.m?js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }
        ]
    },
    target: ['web', 'es5']
};
