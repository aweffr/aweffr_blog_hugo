const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const isProduction = process.argv.includes('production');
const mode = (isProduction) ? 'production' : 'development';
const jsFilename = (isProduction) ? "[name]-[hash:6].bundle.js" : "[name].dev.bundle.js";
const cssFilename = (isProduction) ? "[name]-[hash:6].css" : "[name].dev.css";

const webpackStatFileName = isProduction ? './webpack-stats-prod.json' : './webpack-stats-dev.json';

const config = {
  entry: './src/index',
  output: {
    pathinfo: true,
    path: path.resolve('./dist/webpack_bundles/'),
    filename: jsFilename,
  },
  mode: mode,
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.scss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader', // Translates CSS into CommonJS
          'sass-loader', // Compiles Sass to CSS
        ],
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx', '.tsx', '.ts']
  },
  plugins: [
    new MiniCssExtractPlugin({filename: cssFilename}),
    new CleanWebpackPlugin(),
    new BundleTracker({filename: webpackStatFileName}),
  ],
  devtool: 'source-map',
  devServer: {
    hot: true,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
      "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization"
    },
    publicPath: 'http://localhost:8080/'
  },
};

if (!isProduction) {
  config.devServer.publicPath = 'http://localhost:8080/';
  config.output.publicPath = 'http://localhost:8080/';
} else {
  config.externals = {
    react: 'React',
    'react-dom': 'ReactDOM',
  }
}

module.exports = config;
