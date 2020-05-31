<template>
  <div id="app" class="main">
    <div class="mainContainer">
      <h1 class="mainTitle">Markdown Editor</h1>

      <select id="documents" v-model="selectedValue" v-if="docs.length > 0">
        <option v-for="doc in docs" :value="doc.id">{{ doc.name }}</option>
      </select>

      <br />
      <br />

      <button class="btn btn-dark" @click="openClosePreview">Önizlemeyi Aç/Kapat</button>

      <hr />

      <div class="row">
        <div class="col">
          <h5>Girdi</h5>
          <hr />
          <input type="text" placeholder="Doküman İsmi" v-model="name" v-if="authStatus === 1" />
          <br />
          <br />
          <textarea-autosize
            class="form-control"
            ref="myTextarea"
            v-model="source"
            :min-height="420"
          />
          <br />
          <button
            class="btn btn-warning"
            @click="save"
            v-if="authStatus === 1 && selectedValue === ''"
          >Kaydet</button>
          <button
            class="btn btn-warning"
            @click="saveWithoutLogin"
            v-else-if="authStatus === 0 && selectedValue === ''"
          >Kaydet</button>
          <button
            class="btn btn-warning"
            @click="update(selectedValue)"
            v-else-if="authStatus === 1 && selectedValue != ''"
          >Güncelle</button>
          <button class="btn btn-danger" @click="removeDoc(selectedValue)">Sil</button>
          <button class="btn btn-dark" @click="download">PDF Olarak İndir</button>
        </div>
        <div class="col" v-if="previewStatus === 1">
          <h5>Önizleme</h5>
          <hr />
          <vue-simple-markdown :source="source"></vue-simple-markdown>
        </div>
      </div>
      <br><br><br>
      <!-- <div v-for="doc in docs">
        {{doc}}
        <a @click="removeDoc(doc.id)">X</a>
      </div> -->
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
      name: "",
      selectedValue: "",
      status: 0,
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

  watch: {
    selectedValue() {
      for (let i = 0; i < this.docs.length; i++) {
        if (this.docs[i].id == this.selectedValue) {
          this.name = this.docs[i].name;
          this.source = this.docs[i].text;
        }
      }
    }
  },

  methods: {
    saveWithoutLogin() {
      localStorage.setItem("sourceMarkdown", this.source);
    },

    save() {
      let data = { name: this.name, text: this.source };
      this.$http
        .post("/docs", data, { headers: { Authorization: this.token } })
        .then(response => {
          this.getDocs();
        })
        .catch(function(error) {
          console.log(error);
        });
    },

    update(index) {
      let data = { name: this.name, text: this.source };
      this.$http
        .put("/docs/" + index, data, { headers: { Authorization: this.token } })
        .then(response => {
          this.getDocs();
          console.log(response);
        })
        .catch(function(error) {
          console.log(error);
        });
    },

    checkAuth() {
      this.$http
        .get("/", { headers: { Authorization: this.token } })
        .then(response => {
          let result = response.data.status;
          if (result == true) {
            this.authStatus = 1;
            this.status = 1;
          }
        })
        .catch(function(error) {
          alert(
            "Burada yapılan değişiklikler tarayıcınıza kaydolmaktadır. Verileriniz kaybolabilir."
          );
        });
      if (this.status === 0) {
        this.source = localStorage.getItem("sourceMarkdown");
      }
    },

    getDocs() {
      this.$http
        .get("/docs", { headers: { Authorization: this.token } })
        .then(response => {
          this.docs = response.data.docs;
        })
        .catch(function(error) {
          console.log(error);
        });
    },

    removeDoc(index) {
      this.$http
        .delete("/docs/" + index, { headers: { Authorization: this.token } })
        .then(response => {
          this.getDocs();
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
