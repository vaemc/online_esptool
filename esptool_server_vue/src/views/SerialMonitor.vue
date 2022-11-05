<template>
  <div>
    <v-select
      @click="portListRefresh"
      :items="portList"
      label="端口"
    ></v-select>
    <v-select :items="baudRateList" label="波特率"></v-select>
    <v-btn block @click="ok" depressed color="primary">打开</v-btn>

    <div style="margin-top: 10px" v-html="info"></div>
  </div>
</template>

<script>
import * as easings from "vuetify/lib/services/goto/easing-patterns";
export default {
  data() {
    return {
      portList: [],
      baudRateList: ["300","600","750","1200","2400","4800","9600","19200","38400","57600","115200","230400","460800","500000","921600","1000000","2000000"],
      info: "",
    };
  },
  mounted() {
    this.axios.get("port_list").then((res) => {
      this.portList = res.data;
    });
  },
  methods: {
    portListRefresh() {
      this.axios.get("port_list").then((res) => {
        this.portList = res.data;
      });
    },
    ok() {
      const wsuri = "ws://192.168.5.190:8081/";
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