const BundleTracker = require('webpack-bundle-tracker');

const isProd = () => {
  return process.env.NODE_ENV === 'production';
}

module.exports = {
  configureWebpack: config => {
    const filename = isProd() ? './webpack-stats-prod.json' : './webpack-stats-dev.json';
    config.plugins.push(new BundleTracker({filename: filename}));
  },
  devServer: {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
      "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization"
    }
  }
};

if (!isProd()) {
  module.exports.publicPath = 'http://localhost:8081/';
}
