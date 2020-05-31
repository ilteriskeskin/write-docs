import Vue from 'vue'
import App from './App.vue'
import VueRouter from "vue-router";
import { routes } from './routes';
import VueSimpleMarkdown from 'vue-simple-markdown';
import VueTextareaAutosize from 'vue-textarea-autosize';

import axios from 'axios'
let baseURL = 'https://write-api.ilteris.ninja/'
//let baseURL = 'http://localhost:5000/'

Vue.prototype.baseURL = baseURL;
Vue.prototype.$http = axios.create({
    baseURL: baseURL,
})

Vue.use(VueRouter);
Vue.use(VueSimpleMarkdown);
Vue.use(VueTextareaAutosize);

const router = new VueRouter({
    routes,
    mode: 'history',
});


new Vue({
    el: '#app',
    router,
    render: h => h(App)
})