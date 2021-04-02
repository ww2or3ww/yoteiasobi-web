<template>
  <v-row justify="center">
    <v-col v-if="id == null">
      <Calendars />
    </v-col>
    <v-col v-else>
      <Calendar :id="id" />
    </v-col>
  </v-row>
</template>

<script>
import Calendars from '~/components/Calendars.vue'
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
