<template>
    <div>
        <v-file-input filled v-model="firmware.file" label="选择固件"></v-file-input>
        <v-select filled :items="boardList" v-model="firmware.info.board" label="板子类型"></v-select>

        <v-text-field v-model="firmware.info.description" label="描述" filled></v-text-field>

        <v-textarea filled label="烧录命令" v-model="firmware.info.cmd"
            hint="注意：请将命令中的端口换成  ${PORT}  Bin文件路径换成  ${BIN}  ，并省略esptool.exe前缀">

            <template v-slot:append-outer>
                <div>
                    <v-btn text @click="firmware.info.cmd += 'write_flash 0x0 ${BIN}'" color="primary">
                        默认命令
                    </v-btn>
                    <v-btn text @click="firmware.info.cmd += '${PORT}'" color="primary">
                        ${PORT}
                    </v-btn>
                    <v-btn text @click="firmware.info.cmd += '${BIN}'" color="primary">
                        ${BIN}
                    </v-btn>
                </div>
            </template>
        </v-textarea>
    </div>
</template>
<script>
import { uid } from 'uid';
import moment from "moment";
export default {
    // props: {
    //     firmware: {}
    // },
    // name: "FirmwareUpload",
    data() {
        return {
            firmware: {
                file: null,
                info: {
                    filename: "",
                    alias: uid(32),
                    board: "ESP32",
                    cmd: "",
                    description: "",
                    time: moment().format("YYYY-MM-DD HH:mm:ss"),
                }
            },
            boardList: ["ESP8266", "ESP8285", "ESP32", "ESP32-C2", "ESP32-C3", "ESP32-S2", "ESP32-S3"],
        }
    },
    methods: {
        cc(a) {
            console.info(a);
        }
    }

}
</script>