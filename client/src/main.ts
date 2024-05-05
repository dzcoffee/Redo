import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import router from '@/router'
import Toast from "vue-toastification";
import vuetify from '@/plugins/vuetify'

import "vue-toastification/dist/index.css";
import '@/main.css';

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast)
app.use(vuetify)

app.mount('#app')
