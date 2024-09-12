import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/components/LoginView.vue";
import MainView from "@/components/MainView.vue";
import DiseaseDiagnosis from "@/components/DiseaseDiagnosis.vue";
import AppChatbot from "@/components/AppChatbot.vue";
import GraphView from "@/components/GraphView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/LoginView",
            name: "Login",
            component: LoginView,
        },
        {
            path: "/",
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
        {
            path: "/Graph",
            name: "Graph",
            component: GraphView,
        }
    ],
});

export default router;