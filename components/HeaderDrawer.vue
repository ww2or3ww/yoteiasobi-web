<template>
  <v-card>
    <v-list-item-action>
      <v-app-bar-nav-icon
        @click.stop="$emit('onClickFromDrawer')"
        class="navicon" />
    </v-list-item-action>
    <v-list>

      <v-list-item to="/">
        <v-list-item-action>
          <v-icon>mdi-home-outline</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            TOP
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider />

      <v-list-item to="/calendars">
        <v-list-item-action>
          <v-icon>mdi-calendar-month</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            Calendar
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item to="/about">
        <v-list-item-action>
          <v-icon>mdi-comment-question-outline</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            About
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider v-if="isAdmin" />
      <v-list-item  v-if="isAdmin" to="/users">
        <v-list-item-action>
          <v-icon>mdi-account-group</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            User
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
      isAdmin: false,
    }
  },
  mounted () {
    this.isAdmin = this.$auth_is_admin()
  },
}
</script>
<style>
.navicon {
  margin-left: 10px;
}
</style>
