import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Toaster } from "vue-sonner";
import router from './router'
import App from './App.vue'
import './index.css'

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.use(Toaster);
app.mount('#app')
