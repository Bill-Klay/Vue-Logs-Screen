// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Root',
    component: () => import('@/components/Home.vue'),
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('token')) {
        next(); // Allow access to the route
      } else {
        next('/login'); // Redirect to another route (e.g., home) if JWT is not valid
      }
    },
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/components/Home.vue'),
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('token')) {
        next();
      } else {
        next('/login');
      }
    },
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    beforeEnter: (to, from ,next) => {
      if (localStorage.getItem('token')) next('/home');
      else next();
    }   
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
