<template>
  <div class="main">
    <section class="section_list">
      <v-card-title>
        <v-text-field
          v-model="search"
          type="text"
          single-line
          hide-details
        >
          <template v-slot:append>
            <v-btn @click="onClickSearch">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
            <v-btn
              :disabled="selectedUser==null"
              @click="onClickDetail">
              <v-icon>mdi-account-details</v-icon>
            </v-btn>
          </template>
        </v-text-field>
      </v-card-title>
      <v-data-table
        v-model="selected"
        v-if="users"
        :headers="headers" 
        :items="users"
        item-key="id"
        hide-default-footer
        @click:row="onClickRow"
      >
        <template v-slot:item.imageAddress="{ item }">
          <v-avatar>
            <v-img :src="item.imageAddress"></v-img>
          </v-avatar>
        </template>
      </v-data-table>
      <v-data-table
        v-else
        loading
        loading-text="Loading... Please wait"
        hide-default-footer
      >
      </v-data-table>
    </section>
    
  </div>
</template>
<script>
import { API } from 'aws-amplify'
export default {
  data() {
    return {
      headers: [
        { text: "icon", value: "imageAddress", sortable: false },
        { text: 'name', value: 'name' },
        { text: 'email', value: 'email' },
        { text: 'comment', value: 'comment' },
      ],
      users: null,
      search: "",
      selectedUser: null,
      selected: []
    }
  },
  mounted () {
    this.initialize()
  },
  methods: {
    async initialize() {
      this.users = await this.getUsers()
    },
    async getUsers() {
      try {
        const count = 10
        const users = await API.get(
          process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
          '/profile?count=' + count + '&search=' + this.search
        )
        users.forEach(async (user, i) => {
          user['id'] = i
          user['imageAddress'] = await this.$auth_get_picture_address_from_storage(user)
        })
        console.log(users)
        
        return users
      } catch (error) {
        console.log(error)
        this.users = null
      }
    },
    async onClickSearch() {
      this.selectedUser = null
      this.selected = []
      this.users = null
      this.users = await this.getUsers()
    },
    onClickRow(item) {
      this.selectedUser = item
      this.selected = [item]
      console.log(this.selectedUser)
    },
    onClickDetail() {
      console.log(this.selectedUser)
      this.$router.push('/userProfile?username=' + this.selectedUser['username'])
    },
  }
}
</script>
<style>
.section_list {
  margin-bottom: 32px;
}
</style>
