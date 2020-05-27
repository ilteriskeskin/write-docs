import Vue from 'vue'
import App from './App.vue'
import VueRouter from "vue-router";
import { routes } from './routes';
import VueSimpleMarkdown from 'vue-simple-markdown';
import VueTextareaAutosize from 'vue-textarea-autosize';

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