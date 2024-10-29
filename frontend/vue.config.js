const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '0.0.0.0',
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://REDACTED_PUBLIC_HOST:7000',
        changeOrigin: true,
      },
    },
  },
});