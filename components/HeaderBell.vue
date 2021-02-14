<template>
  <v-menu offset-y nudge-left="80" rounded="b-lg">
    <template v-slot:activator="{on}">
      <div class="avatar">
        <v-btn icon v-if="isAuthed" v-on="on">
          <v-avatar>
            <v-icon>mdi-bell-outline</v-icon>
          </v-avatar>
        </v-btn>
      </div>
    </template>

    <v-list color="grey darken-2">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            INFORMATION
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider />
      
      <v-list-item @click="onMenuTest">
        <v-list-item-content>
          <v-list-item-title>Test</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      
    </v-list>

  </v-menu>
</template>
<script>
export default {
  data() {
    return {
      isAuthed: true,
    }
  },
  mounted () {
    this.isAuthed = this.$auth_is_authed()
  },
  methods: {
    onMenuTest() {
      console.log("xxxxxxxxxxxxxxxxxxx")
    },
  }
}
</script>
<style>
.avatar {
  margin-right: 10px;
}
</style>
