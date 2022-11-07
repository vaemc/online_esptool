<template>
  <v-app id="inspire">
    <v-system-bar dark color="deep-purple accent-3" app>
      <v-spacer></v-spacer>
      <v-icon>mdi-wifi-strength-4</v-icon>
      <v-icon>mdi-signal-cellular-outline</v-icon>
      <v-icon>mdi-battery</v-icon>
      <span>12:30</span>
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
        <v-list-item @click="toFirmwareFlash" link>
          <v-list-item-icon>
            <v-icon>mdi-database-arrow-right</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>烧录固件 </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="toFirmwareManage" link>
          <v-list-item-icon>
            <v-icon>mdi-database-edit</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>固件管理</v-list-item-title>
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
export default {
  data() {
    return {
      drawer: null,
    };
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
  },
};
</script>