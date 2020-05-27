<template>
  <div id="app">
    <NavbarComponent></NavbarComponent>
    <router-view></router-view>
  </div>
</template>

<script>
import NavbarComponent from './components/NavbarComponent';

export default {
  name: 'app',

  components: {
    NavbarComponent,
  }
}
</script>

<style>

</style>
