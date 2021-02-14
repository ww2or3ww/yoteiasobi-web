<template>
  <v-card>
    <v-btn @click="signout">Sign Out</v-btn>
  </v-card>
</template>

<script>
export default {
  methods: {
    signout() {
      this.$auth_signout()
    }
  }
}
</script>