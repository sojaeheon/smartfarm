import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import store from './store/store'; // Vuex 스토어 임포트
import axios from 'axios'

// Axios 기본 URL 설정
axios.defaults.baseURL = 'http://localhost:7000'; // 혹은 서버 IP를 넣을 수 있습니다.

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')
