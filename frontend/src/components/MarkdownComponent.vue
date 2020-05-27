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
          <button class="btn btn-warning" @click="save">Kaydet</button>
          <button class="btn btn-danger" @click="download">PDF Olarak İndir</button>
        </div>
        <div class="col" v-if="previewStatus === 1">
          <h5>Önizleme</h5>
          <hr />
          <vue-simple-markdown :source="source"></vue-simple-markdown>
        </div>
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
      source: localStorage.getItem("sourceMarkdown")
        ? localStorage.getItem("sourceMarkdown")
        : "# Hello World!",
      previewStatus: 0
    };
  },

  mounted() {
    alert(
      "Burada yapılan değişiklikler tarayıcınıza kaydolmaktadır. Verileriniz kaybolabilir."
    );
  },

  methods: {
    save() {
      localStorage.setItem("sourceMarkdown", this.source);
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
    }
  }
};
</script>

<style>
@import "../assets/css/style.css";
</style>
