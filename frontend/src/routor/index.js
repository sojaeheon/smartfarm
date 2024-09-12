import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/components/LoginView.vue";
import AppChatbot from "@/components/AppChatbot.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "LoginView",
            component: LoginView,
        },
        {
            path: "/AppChatbot",
            name: "AppChatbot",
            component: AppChatbot,
        },
    ],
});

export default router;
