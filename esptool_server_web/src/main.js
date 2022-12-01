import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from '@/plugins/vuetify' // path to vuetify export
import axios from 'axios'
import VueAxios from 'vue-axios'
import { server } from './config'
Vue.config.productionTip = false
Vue.use(VueAxios, axios)
axios.defaults.baseURL = `http://${server.ip}:${server.port}/`
new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
