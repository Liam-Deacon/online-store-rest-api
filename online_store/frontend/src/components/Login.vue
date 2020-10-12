<!-- Based on https://www.positronx.io/create-login-signup-ui-screens-in-vue-js-with-bootstrap/ -->
<template>
    <div>
        <form>
            <h3>Sign In</h3>

            <div class="form-group">
                <label>Email address</label>
                <input type="email" class="form-control form-control-lg" />
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control form-control-lg" />
            </div>

            <button type="submit" class="btn btn-dark btn-lg btn-block text-white">Log in</button>

            <p class="forgot-password text-right mt-2 mb-4">
                <router-link to="/password-reset">Forgot password</router-link>
            </p>

            <div class="social-icons">
                <ul>
                    <li><a href="#"><font-awesome-icon :icon="['fab', 'google']" /></a></li>
                    <li><a href="#"><font-awesome-icon :icon="['fab', 'facebook']" /></a></li>
                    <li><a href="#"><font-awesome-icon :icon="['fab', 'twitter']" /></a></li>
                </ul>
            </div>

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
