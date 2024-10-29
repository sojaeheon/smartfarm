import { createRouter, createWebHistory } from "vue-router";

import SignUpView from "@/components/SignUpView.vue";
import LoginView from "@/components/LoginView.vue";
import MainView from "@/components/MainView.vue";
import DiseaseDiagnosis from "@/components/DiseaseDiagnosis.vue";
import AppChatbot from "@/components/AppChatbot.vue";
import store from '../store/store';

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
            meta: { requiresAuth: true },
        },
        {
            path: "/DiseaseDiagnosis",
            name: "Disease",
            component: DiseaseDiagnosis,
            meta: { requiresAuth: true },
        },
        {
            path: "/AppChatbot",
            name: "Chatbot",
            component: AppChatbot,
            meta: { requiresAuth: true },
        },
    ],
});

router.beforeEach(async (to, from, next) => {
    await store.dispatch('checkSession');
    if (to.name === 'Login' && store.state.isLoggedIn) {
        return next({ name: 'Main' });
    }
    if (to.matched.some(record => record.meta.requiresAuth) && !store.state.isLoggedIn) {
        return next({ name: "Login" });
    }
    next();
});

export default router;
