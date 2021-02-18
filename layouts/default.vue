<template>
  <v-app dark>
    <Header :title="title" />
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import Header from '~/components/Header.vue'
import Footer from '~/components/Footer.vue'
export default {
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      title: 'yoteiasobi'
    }
  }
}
</script>

<style>
.main {
  background-color: #757575;
  padding: 8px;
}
</style>
