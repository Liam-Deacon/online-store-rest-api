// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueHead from 'vue-head'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faGoogle, faTwitter, faFacebook } from '@fortawesome/free-brands-svg-icons'

import 'bootstrap/dist/css/bootstrap.min.css'
import './assets/css/main.css'

import vuetify from './plugins/vuetify'
// import '@babel/polyfill'

import 'vuetify/dist/vuetify.min.css'

// use vue-head to inject custom data into HTML <header>
Vue.use(VueHead)

library.add(faUserSecret)
library.add(faGoogle)
library.add(faFacebook)
library.add(faTwitter)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  vuetify,
  template: '<App/>'
})
