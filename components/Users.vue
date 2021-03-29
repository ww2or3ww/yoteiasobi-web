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
              :disabled="selectedList.length==0"
              @click="onClickDetail">
              <v-icon>mdi-account-details</v-icon>
            </v-btn>
          </template>
        </v-text-field>
      </v-card-title>
      <v-data-table
        v-model="selectedList"
        v-if="users"
        :headers="headers" 
        :items="users"
        item-key="id"
        select-all
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
        { text: "Icon",   value: "imageAddress",  width: "50px", sortable: false },
        { text: 'Name',   value: 'name',          width: "200px" },
        { text: 'Email',  value: 'email' },
      ],
      users: null,
      search: "",
      selectedList: []
    }
  },
  mounted () {
    this.initialize()
  },
  methods: {
    async initialize() {
      this.users = await this.getUsers()
      if (this.users.length > 0) {
        this.selectedList = [this.users[0]]
      }
    },
    async getUsers() {
      try {
        const count = 10
        const users = await API.get(
          process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
          '/profile?count=' + count + '&search=' + this.search
        )
        for (let i = 0; i < users.length; i++) {
          const user = users[i]
          user['id'] = i
          user['imageAddress'] = await this.$auth_get_picture_address_from_storage(user)
        }
        return users
      } catch (error) {
        console.log(error)
        this.users = null
        this.selectedList  = []
      }
    },
    async onClickSearch() {
      this.selectedList = []
      this.users = null
      this.users = await this.getUsers()
      if (this.users.length > 0) {
        this.selectedList = [this.users[0]]
      }
    },
    onClickRow(item) {
      this.selectedList = [item]
    },
    onClickDetail() {
      this.$router.push('/users/' + this.selectedList[0]['username'])
    },
  }
}
</script>
<style>
.section_list {
  margin-bottom: 32px;
}
</style>
