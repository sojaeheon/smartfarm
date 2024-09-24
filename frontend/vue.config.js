const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '0.0.0.0',  // 외부 접속 허용
    port: 80        // 원하는 포트 번호
  }
})
