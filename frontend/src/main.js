import { createApp } from 'vue'
import App from './App.vue'
import router from './routor'
import store from './routor/store'; // Vuex 스토어 임포트

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')
