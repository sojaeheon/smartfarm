import { createApp } from 'vue'
import App from './App.vue'
import router from './routor'


const app = createApp(App)
app.use(router)
app.mount('#app')
