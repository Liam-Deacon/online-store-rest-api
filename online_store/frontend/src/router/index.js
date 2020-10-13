import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/about', component: 'About' },
  { path: '/login', component: 'Login' },
  { path: '/signup', component: 'Register' },
  { path: '/password-reset', component: 'ForgottenPassword' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    name: `${route.component}`,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  routes: routes,
  mode: 'history'
})
