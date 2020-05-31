<template>
  <div id="app">
    <div class="container">
      <nav class="navbar navbar-expand-sm justify-content-center">
        <!-- Links -->
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/markdown">Markdown</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="!token" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="!token" to="/register">Register</router-link>
          </li>
          <li class="nav-item">
            <a id="navA" class="nav-link" v-if="token" @click="logout">Logout</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: "NavbarComponent",

  data() {
    return {
      token: localStorage.getItem("token")
    };
  },

  methods: {
    logout() {
      localStorage.removeItem("token");
      // this.$router.push("/login");
      window.location.href = "/login";
    }
  }
};
</script>

<style>
@import "../assets/css/style.css";
</style>
