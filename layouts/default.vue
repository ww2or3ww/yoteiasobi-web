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
      title: 'YOTEIASOBI'
    }
  }
}
</script>

<style>
.main {
  background-color: #1E1E1E;
  padding: 8px;
}
.common-card-title {
  padding: 0;
  padding-left: 16px;
  border: 0 solid;
}
.common-p-card-title {
  font-size: 20px;
  font-weight: bold;
}
.common-p-card-subtitle {
  font-size: 16px;
  font-weight: bold;
}
</style>
