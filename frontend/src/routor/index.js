import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/components/LoginView.vue";
import AppChatbot from "@/components/AppChatbot.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/Login",
            name: "Login",
            component: LoginView,
        },
        {
            path: "/AppChatbot",
            name: "Chatbot",
            component: AppChatbot,
        },
    ],
});

export default router;
