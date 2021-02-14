<template>
  <div>
    <v-btn @click="signin('Google')">Google</v-btn>
    <v-btn @click="signin('LINE')">LINE</v-btn>
  </div>
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