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
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: "NavbarComponent"
};
</script>

<style>
@import "../assets/css/style.css";
</style>
