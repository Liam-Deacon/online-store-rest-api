<!-- Based on https://www.positronx.io/create-login-signup-ui-screens-in-vue-js-with-bootstrap/ -->
<template>
    <div class="vue-template">
        <form>
            <h3>Sign Up</h3>

            <div class="form-group">
                <label>Full Name</label>
                <input type="text" class="form-control form-control-lg"/>
            </div>

            <div class="form-group">
                <label>Email address</label>
                <input type="email" class="form-control form-control-lg" />
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control form-control-lg" />
            </div>

            <button type="submit" class="btn btn-dark btn-lg btn-block text-white">Register</button>

            <p class="forgot-password text-right">
                Already registered
                <router-link to="/login">sign in?</router-link>
            </p>
        </form>
    </div>
</template>

<script>
export default {
  data () {
    return {}
  }
}
</script>
