// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createVuetify } from 'vuetify'

/**
 * @description
 * Vuetify CSS 플러그인
 */
const vuetify = createVuetify({
  components,
  directives
})

export default vuetify
