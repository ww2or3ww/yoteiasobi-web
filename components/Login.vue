<template>
  <div class="main">
    <section class="section_buttons">
      <v-container>
        <v-row class="flex-column">
          <v-col cols="12">
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
          </v-col>
          <v-col cols="12">
            <v-btn
              color="#607D8B"
              @click="signin('LINE')"
              :disabled="true"
              class="login_buttons"
            >
              <v-icon left dark>mdi-alpha-l-circle </v-icon>
              LINE (*coming soon..)
            </v-btn>
          </v-col>
          <v-col cols="12">
            <v-btn
              color="#607D8B"
              @click="signin('Twitter')"
              :disabled="true"
              class="login_buttons"
            >
              <v-icon left dark>mdi-twitter</v-icon>
              Twitter (*coming soon..)
            </v-btn>
          </v-col>
          <v-col cols="12">
            <v-btn
              color="#607D8B"
              @click="signin('Facebook')"
              :disabled="true"
              class="login_buttons"
            >
              <v-icon left dark>mdi-facebook</v-icon>
              Facebook (*coming soon..)
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </section>
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
<style>
.section_buttons {
  text-align: center;
  margin: 24px;
}
.login_buttons {
  width: 280px;
}
</style>
