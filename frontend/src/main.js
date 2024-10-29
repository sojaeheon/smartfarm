import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/store'; // Vuex 스토어 임포트


const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')
