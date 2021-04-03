<template>
  <v-row justify="center" align="center">
    <v-col>
      <v-card>
        <v-card-title>
          Welcome to YOTEIASOBI
        </v-card-title>
        <v-card-subtitle>
          YOTEI DE ASOBOU !!
        </v-card-subtitle>
        <v-card-text>
          YOTEIASOBI は Googleカレンダー を ゆるく共有できる サーバーレスWebアプリです。
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  methods: {
    test1() {
      console.log(this.$store.state.authdata.user)
    },
  },
}
</script>
