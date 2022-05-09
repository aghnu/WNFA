const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: {
      input: './src/input.js',
      output: './src/output.js'
    },
    output: {
      filename: '[name].bundle.js',
      path: path.resolve(__dirname, 'dist'),
    },

    plugins: [
      new HtmlWebpackPlugin({
        title: "WNFA input interface",
        chunks: ['input'],
        filename: 'input.html'
      }),
      new HtmlWebpackPlugin({
        title: "WNFA output interface",
        chunks: ['output'],
        filename: 'output.html'
      })
    ],

    module: {
      rules: [
        {
          test: /\.s[ac]ss$/i,
          use: [
            "style-loader",
            "css-loader",
            "sass-loader",
          ],
        },
        {
          test: /\.(png|jpe?g|gif)$/i,
          use: [
            {
              loader: 'file-loader',
            },
          ],
        },
      ],
    },
  };