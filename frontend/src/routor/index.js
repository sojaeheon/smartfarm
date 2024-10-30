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


export default router;
