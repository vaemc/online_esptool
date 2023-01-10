<template>
  <div>

    
    <v-select filled @click="portListRefresh" :items="portList" label="端口"></v-select>
    <v-select filled :items="firmwareList" label="固件"></v-select>
    <v-btn block @click="ok" depressed color="primary">上传</v-btn>

    <div style="margin-top: 10px" v-html="info"></div>
  </div>
</template>

<script>
import * as easings from "vuetify/lib/services/goto/easing-patterns";
export default {
  data() {
    return {
      portList: [],
      firmwareList: [],
      info: "",
    };
  },
  mounted() {
    this.axios.get("port_list").then((res) => {
      this.portList = res.data;
    });
    this.axios.get("firmware/query").then(res => {
      this.firmwareList = res.data;
    })
  },
  methods: {
    portListRefresh() {
      this.axios.get("port_list").then((res) => {
        this.portList = res.data;
      });
    },
    ok() {
      const wsuri = "ws://192.168.43.198:8081/";
      this.websock = new WebSocket(wsuri);
      this.websock.onmessage = this.websocketonmessage;

      this.info = "";
    },
    websocketonmessage(e) {
      console.log(e.data);
      this.info += e.data + "<br />";

      // const options = {
      //   duration: 300,
      //   offset: 0,
      //   easing: Object.keys(easings),
      // };
      // this.$vuetify.goTo(100, options);
    },
  },
};
</script>