<template>
  <div>
    <v-btn @click="test">TEST</v-btn>
    <v-btn @click="signin('Google')">Google</v-btn>
    <v-btn @click="signin('LINE')">LINE</v-btn>
  </div>
</template>
<script>
import { Auth, API } from 'aws-amplify'
export default {
  methods: {
    signin(providerName) {
      Auth.federatedSignIn({ provider: providerName })
    },
    async test() {
      console.log('xxxxxxxxxx')
      this.checkCurrentAuthenticatedUser();
      console.log('yyyyyyyyyy')
      let myInit = {
        headers: {},
        response: true,
      };
      let resName = process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name;
      const response = await API.get(resName, '/items', myInit).then(response =>{
        console.log(response)
      }).catch(error =>{
        console.log('error occurred!!')
        console.log(error)
      })
      console.log(response)
      console.log('yyyyyyyyyy')
    },
    
  }
}
</script>