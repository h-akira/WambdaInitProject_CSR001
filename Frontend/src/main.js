import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Protected from './views/Protected.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/protected', name: 'Protected', component: Protected, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

// Simple auth guard
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const response = await fetch('/accounts/status')
      const data = await response.json()

      if (data.authenticated) {
        next()
      } else {
        // Redirect to backend login
        window.location.href = '/accounts/login?next=' + encodeURIComponent(to.fullPath)
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      window.location.href = '/accounts/login?next=' + encodeURIComponent(to.fullPath)
    }
  } else {
    next()
  }
})

const app = createApp(App)
app.use(router)
app.mount('#app')