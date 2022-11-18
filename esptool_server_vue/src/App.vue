<template>
  <v-app id="inspire">
    <v-system-bar dark color="deep-purple accent-3" app>
      <v-spacer></v-spacer>
      <v-icon>mdi-wifi-strength-4</v-icon>
      <v-icon>mdi-signal-cellular-outline</v-icon>
      <v-icon>mdi-battery</v-icon>
      <span>{{ time }}</span>
    </v-system-bar>
    <v-navigation-drawer v-model="drawer" app>
      <v-list dense>
        <v-list-item @click="toHome" link>
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>首页</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
     
        <v-list-item @click="toFirmwareManage" link>
          <v-list-item-icon>
            <v-icon>mdi-view-grid-plus </v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>固件管理</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="toTools" link>
          <v-list-item-icon>
            <v-icon>mdi-console</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>常用功能</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- <v-list-item @click="toSerialMonitor" link>
          <v-list-item-icon>
            <v-icon>mdi-connection</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>串口</v-list-item-title>
          </v-list-item-content>
        </v-list-item> -->
      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="deep-purple accent-4" dense dark app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>ESP烧入工具</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import moment from 'moment';
export default {
  data() {
    return {
      drawer: null,
      time: "",
    };
  },
  created() {
    setInterval(() => {
      this.time = moment().format('YYYY-MM-DD HH:mm:ss');
    }, 1000)
  },
  methods: {

    toHome() {
      this.$router.push("/");
      this.drawer = false;
    },
    toFirmwareFlash() {
      this.$router.push("/FirmwareFlash");
      this.drawer = false;
    },
    toFirmwareManage() {
      this.$router.push("/FirmwareManage");
      this.drawer = false;
    },
    toSerialMonitor() {
      this.$router.push("/SerialMonitor");
      this.drawer = false;
    },
    toTools() {
      this.$router.push("/Tools");
      this.drawer = false;
    }
  },
};
</script>