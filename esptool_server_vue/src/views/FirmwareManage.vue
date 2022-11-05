<template>
  <div>
    <v-file-input accept="image/*" label="选择固件"></v-file-input>
    <v-text-field label="烧录命令" filled></v-text-field>
    <v-btn block @click="ok" depressed color="primary">添加</v-btn>
  </div>
</template>