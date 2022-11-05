const HtmlWebpackPlugin = require('html-webpack-plugin')
const HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin')
module.exports = {
    publicPath: '',//使用相对路径
    chainWebpack: config => {
      config.plugin('preload')
        .tap(args => {
          args[0].fileBlacklist.push(/\.css/, /\.js/)
          return args
        })
      config.plugin('inline-source')
        .use(require('html-webpack-inline-source-plugin'))
      config
        .plugin('html')
        .tap(args => {
          args[0].title = 'ESP烧入工具'
          args[0].inlineSource = '(\.css|\.js$)'
          return args
        })
    },
    productionSourceMap: false,
    devServer: {
      https: false
    }
  }
