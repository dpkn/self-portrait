module.exports = {
  configureWebpack:{
    module: {
      rules: [
        {
          test: /\.txt$/,
          use: 'raw-loader'
        }
      ]
    }  
  }
}
