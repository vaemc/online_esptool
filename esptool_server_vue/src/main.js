import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from '@/plugins/vuetify' // path to vuetify export
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.config.productionTip = false
Vue.use(VueAxios, axios)
axios.defaults.baseURL = "http://127.0.0.1:5000/"
new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
