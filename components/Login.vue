<template>
  <div class="main">
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
          <v-col cols="12">
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
          <v-col cols="12">
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
          <v-col cols="12">
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
  </div>
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
  margin: 24px;
}
.row_buttons {
  text-align: center;
}
.login_buttons {
  width: 280px;
}
</style>
