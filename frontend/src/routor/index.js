import { createRouter, createWebHistory } from "vue-router";

import SignUpView from "@/components/SignUpView.vue";
import LoginView from "@/components/LoginView.vue";
import MainView from "@/components/MainView.vue";
import DiseaseDiagnosis from "@/components/DiseaseDiagnosis.vue";
import AppChatbot from "@/components/AppChatbot.vue";

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

// 네비게이션 가드 추가
router.beforeEach((to, from, next) => {
    const isAuthenticated = store.state.auth.loggedIn; // 로그인 상태 확인
  
    if (to.meta.requiresAuth && !isAuthenticated) {
      // 인증이 필요한 경로에 접근하려고 할 때 로그인하지 않은 경우
      next({ name: 'Login' });
    } else if (to.name === 'Login' && isAuthenticated) {
      // 로그인 상태인데 로그인 페이지로 이동하려고 할 때
      next({ name: 'Main' });
    } else {
      next(); // 다음 라우트로 이동
    }
});
export default router;
