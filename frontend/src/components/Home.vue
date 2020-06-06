<template>
  <div id="app">
    <a href="https://github.com/ilteriskeskin/write-docs" target="_blank">
      <img src="../assets/images/github.svg" alt="Github Logo">
    </a>

    <div class="container homeMain">
      <div v-for="doc in docs">
        <ul>
          <li>
            <router-link :to="{ name: 'DocDetail', params: { id: doc.id } }">{{ doc.name }}</router-link>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Home",

    data() {
      return {
        docs: {}
      };
    },

    created() {
      this.getDocs();
    },

    methods: {
      getDocs() {
        this.$http
          .get("/public_docs")
          .then(response => {
            console.log(response);
            this.docs = response.data.docs;
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    }
  };
</script>

<style>
  @import "../assets/css/style.css";

  img {
    height: 70px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 50%;
    cursor: pointer;
  }

  img:hover {
    height: 90px;
  }
</style>
