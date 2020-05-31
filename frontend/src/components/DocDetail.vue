<template>
  <div id="app" class="homeMain">
    <div class="container">
      <h3>{{ doc.name }}</h3>
      <hr>
      <vue-simple-markdown :source="doc.text"></vue-simple-markdown>
    </div>
  </div>
</template>

<script>
export default {
  name: "DocDetail",

  data() {
    return {
      id: this.$route.params.id,
      doc: {}
    };
  },

  created() {
    this.getDocs();
  },

  methods: {
    getDocs() {
      this.$http
        .get("/public_docs/" + this.id)
        .then(response => {
          console.log(response);
          this.doc = response.data.doc;
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>

<style>
@import "../assets/css/style.css";
</style>
