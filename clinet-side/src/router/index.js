import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/pages/HomePage.vue"),
    },
    {
      path: "/calendar",
      name: "calendar",
      component: () => import("@/pages/CalendarPage.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/pages/LogInPage.vue"),
    },
    {
      path: "/guide",
      name: "guide",
      component: () => import("@/pages/GuidePage.vue"),
      meta: { requiresAuth: true, role: "guide" },
    },
    {
      path: "/advisor",
      name: "advisor",
      component: () => import("@/pages/AdvisorPage.vue"),
      meta: { requiresAuth: true, role: "advisor" },
    },
    {
      path: '/secretary',
      name: 'secretary',
      component: () => import('@/pages/SecretaryPage.vue'),
      meta: { requiresAuth: true, role: "secretary" },
      props: true
    },
    {
      path: '/director',
      name: 'director',
      component: () => import('@/pages/DirectorPage.vue'),
      meta: { requiresAuth: true, role: "director" },
    },
    {
      path:'/visitor',
      name:'visitor',
      component: () => import('@/pages/VisitorPage.vue'),
      meta: { requiresAuth: true, role: "visitor" },
      props: true
    },
    {
      path: "/403",
      name: "forbidden",
      component: () => import("@/pages/ForbiddenPage.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("@/pages/RegisterPage.vue"),
    },
    {
      path: "/coordinator",
      name: "coordinator",
      component: () => import("@/pages/CoordinatorPage.vue"),
      meta: { requiresAuth: true, role: "coordinator" },
    }
  ],
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Wait for auth state to initialize
  if (!authStore.authInitialized) {
    await authStore.initializeAuthState();
  }

  const isAuthenticated = authStore.isLoggedIn;
  const userRole = authStore.userRole;

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next("/login");
  }

  if (to.meta.role && to.meta.role !== userRole) {
    return next("/403");
  }

  next();
});

export default router;
