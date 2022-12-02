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
    <FirmwareUpload ref="firmwareUpload" />
    <v-btn block @click="addFirmwareBtn" depressed color="primary">添加</v-btn>
    <v-dialog v-model="firmwareUpdateDialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">修改 {{ firmwareUpdateDialogTitle }}</span>
        </v-card-title>
        <v-container>
          <FirmwareUpload ref="firmwareUpload" />
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="firmwareUpdateDialogClose">
            取消
          </v-btn>
          <v-btn color="primary" text @click="firmwareUpdateDialogSave">
            保存
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-data-table style="margin-top: 10px" :headers="headers" :items="firmwareList" sort-by="calories"
      class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>固件列表</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>

          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5">确定删除&nbsp<span style="color:red">{{ selectedItem.filename }}</span>&nbsp吗
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
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon small class="mr-2" @click="deleteItem(item)"> mdi-delete </v-icon>
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
          <v-progress-linear v-if="flashProgressEnable" height="10" v-model="flashProgress" value="10"
            striped></v-progress-linear>
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

            <v-btn block @click="flashBtn" :loading="flashing" :disabled="flashing" depressed color="primary">烧录
            </v-btn>
            <v-textarea style="margin-top: 15px;" id="outputInfo" outlined rows="7" v-model="outputInfo"></v-textarea>
          </div>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>
<script>
import moment from "moment";
import balanced from "balanced-match"
import { server } from '../config'
import FirmwareUpload from '../components/FirmwareUpload.vue'

export default {
  components: {
    FirmwareUpload
  },
  data: () => ({
    flashProgress: 0,
    flashProgressEnable: false,
    flashing: false,
    outputInfo: "",
    defaultCmd: "esptool.exe write_flash 0x0 ${BIN}",
    selectPort: "",
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
    firmwareUpdateDialogTitle: "",
    firmwareUpdateDialog: false,
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
      { text: "烧入命令", sortable: false, value: "cmd" },
      { text: "添加时间", value: "time" },
      { text: "操作", value: "actions", sortable: false },
    ],
    desserts: [],
    firmwareList: [],
    selectedIndex: -1,
    selectedItem: {},
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
    flashBtn() {
      if (this.selectPort == "") {
        this.snackbar = true;
        this.snackbarText = "请选择端口";
        return;
      }
      this.axios.post("firmware/flash?port=" + this.selectPort, this.selectItem).then(res => {
        console.info(res.data);
        this.info = "";
        this.outputInfo = "";
        this.initWebSocket();
        this.flashing = true;


      })
    },
    initWebSocket() {
      const wsuri = `ws://${server.ip}:8083`;
      this.websock = new WebSocket(wsuri);
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
    },
    websocketonerror() {
      this.initWebSocket();
    },
    websocketonmessage(e) {
      console.info(e.data);
      this.outputInfo += e.data + "\n";
      const outputInfo = document.getElementById('outputInfo');
      outputInfo.scrollTop = outputInfo.scrollHeight;
      let matchResult = balanced('... (', ' %)', e.data)
      if (matchResult != undefined) {
        this.flashProgressEnable = true;
        this.flashProgress = parseInt(matchResult.body);
      }
    },
    websocketclose(e) {
      console.log('close');
      this.flashing = false;
      this.flashProgressEnable = false;
      this.flashProgress = 0;
    },
    addFirmwareBtn() {


      console.info(this.$refs.firmwareUpload.firmware);
      let firmware = this.$refs.firmwareUpload.firmware;

      if (firmware.file == null) {
        this.snackbar = true;
        this.snackbarText = "请选择文件";
        return;
      }
      if (firmware.info.board == "") {
        this.snackbar = true;
        this.snackbarText = "请选择板子类型";
        return;
      }
      if (firmware.info.description == "") {
        this.snackbar = true;
        this.snackbarText = "请输入描述";
        return;
      }
      if (firmware.info.cmd == "") {
        this.snackbar = true;
        this.snackbarText = "请输入烧入命令";
        return;
      }
      firmware.info.alias = firmware.info.alias + "." + firmware.file.name.split(".").pop();


      let formData = new FormData();
      formData.append("file", firmware.file);
      formData.append("alias", firmware.info.alias);
      firmware.info.filename = firmware.file.name;

      this.axios.post("/upload/file", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      this.axios.post("firmware/save", firmware.info).then((res) => {
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
      
      this.selectedIndex = this.firmwareList.indexOf(item);
      this.selectedItem = item;
      this.firmwareUpdateDialog = true;
      this.firmwareUpdateDialogTitle = item.filename;
    },
    flashItem(item) {
      this.flashDialog = true;
      this.selectItem = item;



    },
    deleteItem(item) {
      this.selectedIndex = this.firmwareList.indexOf(item);
      this.selectedItem = item;
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.firmwareList.splice(this.selectedIndex, 1);
      this.closeDelete();
      this.axios.delete("firmware/delete/" + this.selectedItem.id).then(res => {
        this.snackbar = true;
        this.snackbarText = "删除成功";
      })
    },

    firmwareUpdateDialogClose() {
      this.firmwareUpdateDialog = false;

    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.selectedItem = Object.assign({}, this.defaultItem);
        this.selectedIndex = -1;
      });
    },

    firmwareUpdateDialogSave() {

      this.firmwareUpdateDialogClose();
    },
  },
};
</script>