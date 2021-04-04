<template>
  <v-row justify="center" align="center">
    <v-col>
      <v-card>
        <v-card-title>
          Welcome to YOTEIASOBI
        </v-card-title>
        <v-card-subtitle>
          よてい で あそぼう！
        </v-card-subtitle>
        <v-card-text>
          YOTEIASOBI は Googleカレンダー を "ゆるっと共有" できる サーバーレスWebアプリです。
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
