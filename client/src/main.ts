import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import router from '@/router'
import Toast from 'vue-toastification'
import vuetify from '@/plugins/vuetify'

import 'vue-toastification/dist/index.css'
import '@/main.css'

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.use(Toast)
app.use(vuetify)

app.mount('#app')
