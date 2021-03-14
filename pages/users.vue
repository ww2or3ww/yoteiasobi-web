<template>
  <v-row justify="center" align="center">
    <v-col v-if="id == null">
      <Users />
    </v-col>
    <v-col v-else cols="12" sm="8" md="6">
      <User :id="id" />
    </v-col>
  </v-row>
</template>

<script>
import Users from '~/components/Users.vue'
import User from '~/components/User.vue'
export default {
  data() {
    return {
      id: null,
    }
  },
  watch: {
    $route (to, from) {
      if (to.params) {
        this.id = to.params.id
      }
    }
  },
  mounted () {
    if (this.$route.params ) {
      this.id = this.$route.params.id
    }
  }
}
</script>
