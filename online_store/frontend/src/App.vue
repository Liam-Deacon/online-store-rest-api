<template>
  <div class="vue-template">
    <!-- Navigation -->
    <nav class="navbar shadow bg-white rounded justify-content-between flex-nowrap flex-row fixed-top">
      <div class="container">
        <router-link class="navbar-brand nav-link" to="/">Online Gift Store</router-link>
        <ul class="nav navbar-nav flex-row float-right">
          <li class="nav-item">
            <router-link class="nav-link pr-3" to="/login">Sign in</router-link>
          </li>
          <li class="nav-item">
            <router-link class="btn btn-outline-primary" to="/signup">Sign up</router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Main -->
    <div class="App">
      <div class="vertical-center">
        <div class="inner-block">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {

    }
  },
  head: {
    title: {
      inner: 'Online Store App',
      separator: '|',
      complement: 'Example by Liam Deacon'
    },
    link: [
      { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/assets/logo.png' },
      { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/assets/logo.png' }
    ]
  }
}
</script>
