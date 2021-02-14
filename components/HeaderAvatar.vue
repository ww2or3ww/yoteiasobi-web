<template>
  <v-menu offset-y rounded="b-lg">
    <template v-slot:activator="{on}">
      <div class="avatar">
        <v-btn icon v-if="isAuthed" v-on="on">
          <v-avatar>
            <img class="avatar icon"
              :src="pictureAddress"
            >
          </v-avatar>
        </v-btn>
        <v-btn icon v-else v-on="on">
          <v-icon>mdi-account-question-outline</v-icon>
        </v-btn>
      </div>
    </template>

    <v-list color="grey darken-2">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            {{name}}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{mailAddress}}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider />
      
      <v-list-item v-if="isAuthed" to="/user">
        <div class="list_item_icon">
          <v-icon>mdi-account-edit</v-icon>
        </div>
        <v-list-item-content>
          <v-list-item-title>PROFILE</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      
      <v-list-item v-if="isAuthed" @click="onMenuLogout">
        <div class="list_item_icon">
          <v-icon>mdi-logout</v-icon>
        </div>
        <v-list-item-content>
          <v-list-item-title>LOG OUT</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item v-else to="/login">
        <div class="list_item_icon">
          <v-icon>mdi-login</v-icon>
        </div>
        <v-list-item-content>
          <v-list-item-title>LOG IN</v-list-item-title>
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
      name: "Guest", 
      mailAddress: "---",
      pictureAddress: "", 
    }
  },
  mounted () {
    this.isAuthed = this.$auth_is_authed()
    if (this.isAuthed != null) {
      this.name = this.$auth_get_name()
      this.mailAddress = this.$auth_get_email()
      this.pictureAddress = this.$auth_get_picture()
    }
  },
  methods: {
    onMenuLogout() {
      this.$auth_signout()
    }
  }
}
</script>
<style>
.avatar {
  margin-right: 10px;
}
.avatar.icon {
  margin-left: 10px;
  padding: 5px;
}
.list_item_icon {
  margin-right: 10px;
}
</style>
