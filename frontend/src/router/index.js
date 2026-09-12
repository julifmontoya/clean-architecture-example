import { createRouter, createWebHistory } from "vue-router";
import homeRoutes from "@/modules/home/presentation/router";
import catalogRoutes from "@/modules/catalog/presentation/router";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        ...homeRoutes,
        ...catalogRoutes,
    ],
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition;
        }

        return { top: 0 };
    },
});

export default router;