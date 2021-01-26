<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <div class="text-center">
        <logo />
        <vuetify-logo />
      </div>
      <v-card>
        <v-card-title class="headline">
          Welcome to the Vuetify + Nuxt.js template
        </v-card-title>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" nuxt to="/inspire"> Continue </v-btn>
          <v-btn @click="signout">Sign Out</v-btn>
          <v-btn @click="test">TEST</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import Logo from '~/components/Logo.vue'
import VuetifyLogo from '~/components/VuetifyLogo.vue'
import { Auth, API } from 'aws-amplify'

export default {
  middleware: 'auth',
  components: {
    Logo,
    VuetifyLogo,
  },
  methods: {
    signout() {
      Auth.signOut()
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
    
    checkCurrentAuthenticatedUser() {
      Auth.currentAuthenticatedUser().then(
        data => {
          console.log(data)
        }
      ).catch(
        data => {
          console.log(data)
        }
      );
    },

  }
}
</script>
