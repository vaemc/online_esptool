<template>
  <div>



    <v-snackbar v-model="snackbar">
      {{ snackbarText }}

      <template v-slot:action="{ attrs }">
        <v-btn color="pink" text v-bind="attrs" @click="snackbar = false">
          关闭
        </v-btn>
      </template>
    </v-snackbar>

    <v-file-input filled v-model="file" label="选择固件"></v-file-input>
    <!-- <v-select :items="boardList" v-model="firmware.board" label="板子类型" filled></v-select> -->
    <v-select filled :items="boardList" v-model="firmware.board" label="板子类型"></v-select>

    <v-text-field v-model="firmware.description" label="描述" filled></v-text-field>

    <v-textarea filled label="烧录命令" v-model="firmware.cmd"
      hint="注意：请将命令中的端口换成  ${PORT}  Bin文件路径换成  ${BIN}  ，并省略esptool.exe前缀">

      <template v-slot:append-outer>
        <div>
          <v-btn text @click="firmware.cmd += 'write_flash 0x0 ${BIN}'" color="primary">
            默认命令
          </v-btn>
          <v-btn text @click="firmware.cmd += '${PORT}'" color="primary">
            ${PORT}
          </v-btn>
          <v-btn text @click="firmware.cmd += '${BIN}'" color="primary">
            ${BIN}
          </v-btn>
        </div>
      </template>
    </v-textarea>
    <v-btn block @click="addBtn" depressed color="primary">添加</v-btn>

    <v-data-table style="margin-top: 10px" :headers="headers" :items="firmwareList" sort-by="calories"
      class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>固件列表</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>

          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5">确定删除&nbsp<span style="color:red">{{ editedItem.filename }}</span>&nbsp吗
              </v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete">取消</v-btn>
                <v-btn color="blue darken-1" text @click="deleteItemConfirm">确定</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="flashItem(item)"> mdi-flash </v-icon>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
      </template>
      <!-- <template v-slot:no-data>
        <v-btn color="primary" @click="initialize"> Reset </v-btn>
      </template> -->
    </v-data-table>

    <v-row justify="center">
      <v-dialog v-model="flashDialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card>
          <v-toolbar dark color="primary">
            <v-btn icon dark @click="flashDialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>{{ selectItem.filename }}</v-toolbar-title>
            <v-spacer></v-spacer>

          </v-toolbar>
          <v-list three-line subheader>
            <v-subheader>{{ selectItem.filename }}</v-subheader>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>描述</v-list-item-title>
                <v-list-item-subtitle>{{ selectItem.description }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>板子类型</v-list-item-title>
                <v-list-item-subtitle>{{ selectItem.board }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>命令</v-list-item-title>
                <v-list-item-subtitle>{{ selectItem.cmd }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <div style="margin: 5px">
            <v-select filled @click="portListRefresh" @change="portChange" :items="portList" label="端口"></v-select>

            <v-btn block @click="flashBtn" depressed color="primary">烧录</v-btn>
            <v-btn block @click="aaaaa" depressed color="primary">esptool</v-btn>
            <div style="margin-top: 10px" v-html="info"></div>
            <v-textarea id="outputInfo" outlined rows="10" 
              v-model="outputInfo"></v-textarea>
          </div>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>
<script>
import moment from "moment";

function uuidv4() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
    (
      c ^
      (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
    ).toString(16)
  );
}

export default {
  data: () => ({
    outputInfo: "",
    defaultCmd: "esptool.exe write_flash 0x0 ${BIN}",
    selectPort: "",
    info: "",
    portList: [],
    selectItem: "",
    flashDialog: false,
    boardList: ["ESP8266", "ESP8285", "ESP32", "ESP32-C2", "ESP32-C3", "ESP32-S2", "ESP32-S3"],
    snackbarText: "",
    snackbar: false,
    file: null,
    firmware: {
      filename: "",
      alias: "",
      board: "ESP32",
      cmd: "",
      description: "",
      time: "",
    },
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "文件名称",
        align: "start",
        sortable: false,
        value: "filename",
      },
      { text: "板子类型", value: "board" },
      { text: "描述", sortable: false, value: "description" },
      { text: "烧入命令", sortable: false, value: "cmd", width: 500 },
      { text: "添加时间", value: "time" },
      { text: "操作", value: "actions", sortable: false },
    ],
    desserts: [],
    firmwareList: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      calories: 0,
      fat: 0,
      carbs: 0,
      protein: 0,
    },
    defaultItem: {
      name: "",
      calories: 0,
      fat: 0,
      carbs: 0,
      protein: 0,
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
  },
  mounted() {
    this.axios.get("firmware/query").then(res => {
      //console.info(res.data);
      this.firmwareList = res.data;
    })
  },
  methods: {
    portChange(item) {
      this.selectPort = item;
    },
    aaaaa() {
      const wsuri = "ws://localhost:8083";
      this.websock = new WebSocket(wsuri);
      this.websock.onmessage = this.websocketonmessage;



    },
    flashBtn() {
      if (this.selectPort == "") {
        this.snackbar = true;
        this.snackbarText = "请选择端口";
        return;
      }
      this.axios.post("firmware/flash?port=" + this.selectPort, this.selectItem).then(res => {
        console.info(res.data);
        this.info = "";



      })
    },
    websocketonmessage(e) {
      console.log(e.data);
      // this.info += e.data + "<br />";

      this.outputInfo += e.data + "\n";

      const outputInfo = document.getElementById('outputInfo');
      outputInfo.scrollTop = outputInfo.scrollHeight;
      // const options = {
      //   duration: 300,
      //   offset: 0,
      //   easing: Object.keys(easings),
      // };
      // this.$vuetify.goTo(100, options);
    },
    addBtn() {
      if (this.file == null) {
        this.snackbar = true;
        this.snackbarText = "请选择文件";
        return;
      }
      if (this.firmware.board == "") {
        this.snackbar = true;
        this.snackbarText = "请选择板子类型";
        return;
      }
      if (this.firmware.description == "") {
        this.snackbar = true;
        this.snackbarText = "请输入描述";
        return;
      }
      if (this.firmware.cmd == "") {
        this.snackbar = true;
        this.snackbarText = "请输入烧入命令";
        return;
      }

      let uuid = uuidv4() + "." + this.file.name.split(".").pop();
      let formData = new FormData();
      formData.append("file", this.file);
      formData.append("alias", uuid);
      //console.info(this.file.name);
      this.firmware.alias = uuid;
      this.firmware.filename = this.file.name;
      this.firmware.time = moment().format("YYYY-MM-DD HH:mm:ss");
      this.axios.post("/upload/file", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      this.axios.post("firmware/save", this.firmware).then((res) => {
        this.snackbar = true;
        this.snackbarText = "添加成功";

        this.firmwareList.push(res.data);
      });


    },
    portListRefresh() {
      this.axios.get("port_list").then((res) => {
        this.portList = res.data;
      });
    },
    editItem(item) {
      this.editedIndex = this.firmwareList.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    flashItem(item) {
      this.flashDialog = true;
      this.selectItem = item;



    },
    deleteItem(item) {
      this.editedIndex = this.firmwareList.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.firmwareList.splice(this.editedIndex, 1);
      this.closeDelete();
      this.axios.delete("firmware/delete/" + this.editedItem.id).then(res => {
        this.snackbar = true;
        this.snackbarText = "删除成功";
      })
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.firmwareList[this.editedIndex], this.editedItem);
      } else {
        this.firmwareList.push(this.editedItem);
      }
      this.close();
    },
  },
};
</script>