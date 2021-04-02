<template>
  <v-flex xs12 sm12 md12>
    <v-card>
      <v-card-title class="common-card-title">
        <p class="common-p-card-title" style="margin: 0;">Login</p>
      </v-card-title>
    </v-card>
    <v-card>
      <section class="section_buttons">
        <v-container>
          <v-row class="row_buttons">
            <v-col cols="12">
              <IconButton
                color="#607D8B"
                :callbackClick="signin"
                mytype="Google"
                text="Google"
                icon="mdi-google"
                class="login_buttons"
              />
            </v-col>
            <v-col cols="12" v-show="false">
              <IconButton
                color="#607D8B"
                :callbackClick="signin"
                mytype="LINE"
                text="LINE (T.B.D.)"
                icon="mdi-alpha-l-circle"
                class="login_buttons"
                :isDisabled=true
              />
            </v-col>
            <v-col cols="12" v-show="false">
              <IconButton
                color="#607D8B"
                :callbackClick="signin"
                mytype="Twitter"
                text="Twitter (T.B.D.)"
                icon="mdi-twitter"
                class="login_buttons"
                :isDisabled=true
              />
            </v-col>
            <v-col cols="12" v-show="false">
              <IconButton
                color="#607D8B"
                :callbackClick="signin"
                mytype="Facebook"
                text="Facebook (T.B.D.)"
                icon="mdi-facebook"
                class="login_buttons"
                :isDisabled=true
              />
            </v-col>
          </v-row>
        </v-container>
      </section>
    </v-card>
  </v-flex>
</template>
<script>
import IconButton from '~/components/IconButton.vue'
export default {
  components: {
    IconButton,
  },
  methods: {
    signin(providerName) {
      this.$auth_signin(providerName)
    },
  }
}
</script>
<style>
.section_buttons {
  text-align: center;
  margin: 2px;
}
.row_buttons {
  text-align: center;
}
.login_buttons {
  width: 280px;
}
</style>
