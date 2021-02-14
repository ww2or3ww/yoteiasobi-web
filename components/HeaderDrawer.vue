<template>
  <v-card>
    <v-list-item-action>
      <v-app-bar-nav-icon
        @click.stop="$emit('onClickFromDrawer')"
        class="navicon" />
    </v-list-item-action>
    <v-list>
      <v-list-item
        v-for="(item, i) in items"
        :key="i"
        :to="item.to"
        router
        exact
      >
        <v-list-item-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title v-text="item.title" />
        </v-list-item-content>
      </v-list-item>
      
      <v-divider />
      
      <v-list-item to="/support">
        <v-list-item-action>
          <v-icon>mdi-hand-heart-outline</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            Support
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

    </v-list>
  </v-card>
</template>
<script>
export default {
  data() {
    return {
      items: [
        {
          icon: 'mdi-home-outline',
          title: 'TOP',
          to: '/',
        },
        {
          icon: 'mdi-feature-search-outline',
          title: 'SEARCH',
          to: '/login',
        },
        {
          icon: 'mdi-square-edit-outline',
          title: 'REGIST',
          to: '/login',
        },
      ],
    }
  },
}
</script>
<style>
.navicon {
  margin-left: 10px;
}
</style>
