<template>
  <div class="main">
    <section class="section_list">
      <v-card-title>
        <v-text-field
          type="text"
          single-line
          hide-details
        >
          <template v-slot:append>
            <v-btn @click="onClickSearch">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </template>
        </v-text-field>
      </v-card-title>
      <v-data-table
        v-if="calendars"
        :headers="headers" 
        :items="calendars"
        item-key="id"
        select-all
        hide-default-footer
      >
      </v-data-table>
      <v-data-table
        v-else
        loading
        loading-text="Loading... Please wait"
        hide-default-footer
      >
      </v-data-table>
    </section>
    
    <section class="section_form">
        <v-textarea
          v-model="title"
          label="Title"
          counter="500"
          dense
          class="text_field text-white"
        />
        <v-textarea
          v-model="description"
          label="Description"
          counter="500"
          dense
          class="text_field text-white"
        />
      </v-form>
    </section>
    
    <section class="section_buttons">
      <v-btn
        color="#607D8B"
        @click="onRegist"
        :disabled="isProcessing"
      >
        Regist
        <v-icon right dark>mdi-account-edit-outline</v-icon>
      </v-btn>
    </section>

    <v-overlay :value="isProcessing">
      <v-progress-circular
        :size="100"
        :width="8"
        color="primary"
        indeterminate
      />
    </v-overlay>
    
  </div>
</template>
<script>
import { API, graphqlOperation } from 'aws-amplify'
import { listCalendar2 } from '~/src/graphql/queries'
import { createCalendar2 } from "~/src/graphql/mutations"
export default {
  data() {
    return {
      headers: [
        { text: "icon", value: "imageAddress", sortable: false },
        { text: 'owner', value: 'owner' },
        { text: 'calendarId', value: 'calendarId' },
        { text: 'title', value: 'title' },
        { text: 'description', value: 'description' },
      ],
      calendars: null,
      title: "",
      description: "",
      isProcessing: false,
      message: "",
    }
  },
  mounted () {
    this.initialize()
  },
  methods: {
    async initialize() {
      this.calendars = await this.getItems()
      console.log(this.calendars)
    },
    async getItems() {
      try {
        let calendars = await API.graphql(graphqlOperation(listCalendar2, {
          owner: this.$auth_get_user_id(),
          limit: 10
        }))
        console.log(calendars)
        return calendars.data.listCalendar2.items
      } catch (error) {
        console.log(error)
        this.users = null
      }
    },
    async onClickSearch() {
      this.calendars = await this.getItems()
      console.log(this.calendars)
    },
    onRegist() {
      this.registProcess()
    },
    async registProcess() {
      this.isProcessing = true
      try {
        const inputdata = {
          //owner: this.$auth_get_user_id(),
          calendarId: "calendar-id",
          title: this.title, 
          description: this.description
        }
        console.log(inputdata)
        await API.graphql(graphqlOperation(createCalendar2, {input: inputdata}))
        console.log('create done!')
      } catch (error) {
        this.isProcessing = false
        this.message = "error occured : " + error.message
        console.log('error!')
        console.log(error)
      }
      this.isProcessing = false
    },
  }
}
</script>
<style>
.section_list {
  margin-bottom: 32px;
}
.section_form {
  margin-bottom: 32px;
}
.section_buttons {
  text-align: right;
  margin: 16px 16px 16px 16px;
}
.text_field {
  margin: 16px;
}
.text-gray input{
  color: #ccc !important;
}
.text-white input {
  color: #fff !important;
}
</style>
