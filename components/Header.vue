<template>
  <v-card>
    <v-app-bar fixed app>
      <v-btn icon @click.stop="drawer = !drawer">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-toolbar-title v-text="title" class="toolbar__title"/>
      <v-spacer />
      <HeaderBell />
      <HeaderAvatar />
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
      fixed
      temporary
    >
      <HeaderDrawer v-on:onClickFromDrawer="drawer = !drawer" />
    </v-navigation-drawer>
  </v-card>
</template>
<script>
import HeaderDrawer from '~/components/HeaderDrawer.vue'
import HeaderBell from '~/components/HeaderBell.vue'
import HeaderAvatar from '~/components/HeaderAvatar.vue'
export default {
  components: {
    HeaderDrawer,
    HeaderBell,
    HeaderAvatar,
  },
  props: {
    title: {
      type: String, 
      required: true
    }
  },
  data() {
    return {
      drawer: false,
    }
  },
}
</script>
<style>
.toolbar__title {
  color: #FF0032;
  font-family: 'Train One', sans-serif;
  font-size: 24px;
  font-weight: bold;
}

</style>