<template>
  <div id="app" class="main">
    <div class="mainContainer">
      <h1 class="mainTitle">Markdown Editor</h1>
      <button class="btn btn-dark" @click="openClosePreview">Önizlemeyi Aç/Kapat</button>

      <hr />

      <div class="row">
        <div class="col">
          <h5>Girdi</h5>
          <hr />
          <textarea-autosize
            class="form-control"
            ref="myTextarea"
            v-model="source"
            :min-height="420"
          />
          <br />
          <button class="btn btn-warning" @click="save" v-if="authStatus === 1">Kaydet</button>
          <button class="btn btn-warning" @click="saveWithoutLogin" v-else>Kaydet</button>
          <button class="btn btn-danger" @click="download">PDF Olarak İndir</button>
        </div>
        <div class="col" v-if="previewStatus === 1">
          <h5>Önizleme</h5>
          <hr />
          <vue-simple-markdown :source="source"></vue-simple-markdown>
        </div>
      </div>

      <div v-for="doc in docs">
        {{doc}}
        <a @click="removeDoc(doc.id)">X</a>
      </div>
    </div>
  </div>
</template>

<script>
import jsPDF from "jspdf";

export default {
  name: "MarkdownComponent",
  data() {
    return {
      source: "",
      previewStatus: 0,
      token: localStorage.getItem("token"),
      authStatus: 0,
      docs: {}
    };
  },

  created() {
    this.checkAuth();
    this.getDocs();
  },

  methods: {
    saveWithoutLogin() {

      localStorage.setItem("sourceMarkdown", this.source);
    },

    save() {
      let data = { text: this.source };
      this.$http
        .post("/docs", data, { headers: { Authorization: this.token } })
        .then(response => {
          console.log(response);
        })
        .catch(function(error) {
          console.log(error);
        });
    },

    openClosePreview() {
      if (this.previewStatus === 0) {
        this.previewStatus++;
      } else {
        this.previewStatus--;
      }
    },
    download() {
      var showdown = require("showdown"),
        converter = new showdown.Converter(),
        markdownText = this.source,
        htmlText = converter.makeHtml(markdownText);

      var doc = new jsPDF();
      const html = htmlText;

      doc.fromHTML(html, 15, 15, {
        width: 150
      });
      doc.save("docs.pdf");
    },

    checkAuth() {
      this.$http
        .get("/", { headers: { Authorization: this.token } })
        .then(response => {
          let result = response.data.status;
          if (result == true) {
            console.log("Ok");
            this.authStatus = 1;
          }
        })
        .catch(function(error) {
          (this.source = localStorage.getItem("sourceMarkdown")
            ? localStorage.getItem("sourceMarkdown")
            : "# Hello World!"),
            alert(
              "Burada yapılan değişiklikler tarayıcınıza kaydolmaktadır. Verileriniz kaybolabilir."
            );
        });
    },

    getDocs() {
      this.$http
        .get("/docs", { headers: { Authorization: this.token } })
        .then(response => {
          console.log(response);
          this.docs = response.data.docs;
          this.source = response.data.docs[0].text;
        })
        .catch(function(error) {
          console.log(error);
        });
    },

    removeDoc(index) {
      console.log(index);
      this.$http
        .delete("/docs/" + index, { headers: { Authorization: this.token } })
        .then(response => {
          console.log(response);
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

a {
  cursor: pointer;
  font-weight: bold;
}
</style>
