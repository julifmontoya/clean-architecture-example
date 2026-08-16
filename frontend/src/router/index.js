import { createRouter, createWebHistory } from "vue-router";
import homeRoutes from "@/modules/home/presentation/router";
import catalogRoutes from "@/modules/catalog/presentation/router";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        ...homeRoutes,
        ...catalogRoutes,
    ],
});

export default router;