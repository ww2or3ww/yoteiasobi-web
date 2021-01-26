<template>
  <div>
    <v-btn @click="signin">Sign In</v-btn>
  </div>
</template>
<script>
import { Auth } from 'aws-amplify'
export default {
  methods: {
    signin() {
      Auth.federatedSignIn({ provider: 'Google' })
    }
  }
}
</script>