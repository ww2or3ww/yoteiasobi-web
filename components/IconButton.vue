<template>
  <v-btn
    color="#607D8B"
    @click="signin('Google')"
    class="login_buttons"
  >
    <v-container>
      <v-row>
        <v-col cols="2">
          <v-icon left dark>mdi-google</v-icon>
        </v-col>
        <v-col cols="8">
          Google
        </v-col>
        <v-col></v-col>
      </v-row>
    </v-container>
  </v-btn>
</template>
<script>
export default {
  methods: {
    signin(providerName) {
      this.$auth_signin(providerName)
    },
  }
}
</script>
<style>
.login_buttons {
  width: 280px;
}
</style>
