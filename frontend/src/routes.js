import Home from "./components/Home";
import MarkdownComponent from "./components/MarkdownComponent";

import NotFoundComponent from "./components/NotFoundComponent";

export const routes = [
    { path: '/', component: Home, name: 'Home' },
    { path: '/markdown', component: MarkdownComponent, name: 'MarkdownComponent' },

    { path: '*', component: NotFoundComponent },
];