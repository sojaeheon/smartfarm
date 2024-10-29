import { createRouter, createWebHistory } from "vue-router";

import SignUpView from "@/components/SignUpView.vue";
import LoginView from "@/components/LoginView.vue";
import MainView from "@/components/MainView.vue";
import DiseaseDiagnosis from "@/components/DiseaseDiagnosis.vue";
import AppChatbot from "@/components/AppChatbot.vue";
import store from './store'; // Vuex 스토어 가져오기

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/SignUpView",
            name: "Signup",
            component: SignUpView,
        },
        {
            path: "/",
            name: "Login",
            component: LoginView,
        },
        {
            path: "/MainView",
            name: "Main",
            component: MainView,

        },
        {
            path: "/DiseaseDiagnosis",
            name: "Disease",
            component: DiseaseDiagnosis,

        },
        {
            path: "/AppChatbot",
            name: "Chatbot",
            component: AppChatbot,

        },
    ],
});

// 세션 체크를 위한 beforeEach 가드 추가
router.beforeEach(async (to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // 세션 확인을 위한 Vuex 액션 호출
        await store.dispatch('checkSession');
        
        // 로그인 상태인지 확인
        if (!store.state.isLoggedIn) {
            // 로그인 상태가 아니라면 로그인 페이지로 리다이렉트
            next({ name: "Login" });
        } else {
            next();
        }
    } else {
        next(); // 인증이 필요 없는 페이지는 그대로 이동
    }
});

export default router;
