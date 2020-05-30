import Home from "./components/Home";
import MarkdownComponent from "./components/MarkdownComponent";

import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";

import NotFoundComponent from "./components/NotFoundComponent";

export const routes = [
    { path: '/', component: Home, name: 'Home' },
    { path: '/markdown', component: MarkdownComponent, name: 'MarkdownComponent' },

    { path: '/login', component: Login, name: 'Login' },
    { path: '/register', component: Register, name: 'Register' },

    { path: '*', component: NotFoundComponent },
];