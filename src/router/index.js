// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Root',
    component: () => import('@/views/Home.vue'), // this form of import is lazily loaded
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
    component: () => import('@/views/Home.vue'),
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
    component: () => import('@/views/PowerBI.vue'),
    beforeEnter: (to, from ,next) => {
      if (localStorage.getItem('token')) next('/home');
      else next();
    }   
  },
  {
    path: '/powerbi',
    name: 'PowerBI',
    component: () => import('@/views/PowerBI.vue')
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  },
  {
    path: '/:pathMatch(.*)',
    redirect: '/404'  
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
