import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import FirmwareFlash from '../views/FirmwareFlash.vue'
import FirmwareManage from '../views/FirmwareManage.vue'
import SerialMonitor from '../views/SerialMonitor.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/FirmwareFlash',
    name: 'FirmwareFlash',
    component: FirmwareFlash
  },
  {
    path: '/FirmwareManage',
    name: 'FirmwareManage',
    component: FirmwareManage
  },
  {
    path: '/SerialMonitor',
    name: 'SerialMonitor',
    component: SerialMonitor
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
