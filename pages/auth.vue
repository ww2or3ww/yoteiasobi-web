<template>
  <div>
    <v-btn @click="signin('Google')">Google</v-btn>
    <v-btn @click="signin('LINE')">LINE</v-btn>
  </div>
</template>
<script>
import { Auth } from 'aws-amplify'
export default {
  methods: {
    signin(providerName) {
      Auth.federatedSignIn({ provider: providerName })
    }
  }
}
</script>