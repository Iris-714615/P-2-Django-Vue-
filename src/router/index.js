import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children:[
        {
          path: '/student',
          name: 'student',
          component: () => import('../views/StudentView.vue'),
        },
        {
          path: '/teacher',
          name: 'teacher',
          component: () => import('../views/Teacher.vue'),
        },
        {
          path: '/addteacher',
          name: 'addteacher',
          component: () => import('../views/AddTeacher.vue'),
        },
        {
          path: '/article',
          name: 'article',
          component: () => import('../views/Article.vue'),
        },
        {
          path: '/addarticle',
          name: 'addarticle',
          component: () => import('../views/AddArticle.vue'),
        },
      ]
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue'),
    }
  ],
})

export default router