<template>
  <div>
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
        <v-list-item @click="onMenuTest">
          <v-list-item-content>
            <v-list-item-title>
              INFORMATION
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
  
        <v-divider />
        
        <v-list-item @click="onMenuTest">
          <v-list-item-content>
            <v-list-item-title>T.B.D.</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        
      </v-list>
  
    </v-menu>

    <v-dialog v-model="isShowMessage" width="400">
      <MessageBox
        :callbackBtn="onMessageClose"
        :text="message"
        :isShowCancel="false"
      />
    </v-dialog>
      
  </div>
</template>
<script>
import MessageBox from '~/components/MessageBox.vue'
export default {
  data() {
    return {
      isAuthed: false,
      isShowMessage: false,
      message: "",
    }
  },
  mounted () {
    this.isAuthed = this.$auth_is_authed()
  },
  methods: {
    onMenuTest() {
      this.message = "このベルは今は飾りです。"
      this.isShowMessage = true
    },
    onMessageClose() {
      this.isShowMessage = false
    },
  }
}
</script>
<style>
.avatar {
  margin-right: 10px;
}
</style>
