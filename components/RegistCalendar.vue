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
            <v-btn
              :disabled="selectedItem==null"
              @click="onClickDetail">
              <v-icon>mdi-calendar-month</v-icon>
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
        @click:row="onClickRow"
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
        <v-text-field
          label="Calendar ID*"
          v-model="calendarId"
          :rules="[rules.required]"
          counter="30"
          dense
          class="text_field text-white"
        />
        <v-text-field
          label="Title*"
          v-model="title"
          :rules="[rules.required]"
          counter="50"
          dense
          class="text_field text-white"
        />
        <v-text-field
          label="Address"
          v-model="address"
          counter="50"
          dense
          class="text_field text-white"
        />
        <v-text-field
          label="Tel"
          v-model="tel"
          :rules="[rules.tel]"
          counter="50"
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
      <v-btn
        color="#607D8B"
        @click="onProcess"
        :disabled="isProcessing"
      >
        Process
        <v-icon right dark>mdi-rocket-launch</v-icon>
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
import { listCalendar } from '~/src/graphql/queries'
import { createCalendar, processYoteiasobi } from "~/src/graphql/mutations"
export default {
  data() {
    return {
      headers: [
        { text: "icon", value: "imageAddress", sortable: false },
        { text: 'calendarId', value: 'calendarId' },
        { text: 'title', value: 'title' },
      ],
      calendars: null,
      calendarId: "",
      title: "",
      description: "",
      address: "",
      tel: "",
      selectedItem: null,
      isProcessing: false,
      message: "",
      rules: {
        required: value => !!value || 'Required.',
        tel: value => {
          const pattern = /^[0-9]{10,11}$/
          return (value.length == 0 || pattern.test(value)) || 'Invalid TEL.'
        },
      }
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
        let calendars = await API.graphql(graphqlOperation(listCalendar, {
          owner: this.$auth_get_user_id(),
          //calendarId: {
          //  beginsWith: "calendar"
          //},
          limit: 5
        }))
        console.log(calendars)
        return calendars.data.listCalendar.items
      } catch (error) {
        console.log(error)
        this.users = null
      }
    },
    async onClickSearch() {
      this.selectedItem = null
      this.calendars = await this.getItems()
      console.log(this.calendars)
    },
    onClickRow(item) {
      this.selectedItem = item
    },
    onClickDetail() {
      this.$router.push('/calendar?id=' + this.selectedItem['calendarId'])
    },

    async onRegist() {
      this.isProcessing = true
      try {
        const inputdata = {
          owner: this.$auth_get_user_id(),
          calendarId: this.calendarId,
          title: this.title, 
          description: this.description,
          address: this.address,
          tel: this.tel
        }
        console.log(inputdata)
        const res = await API.graphql(graphqlOperation(createCalendar, {input: inputdata}))
        console.log('create done!')
        console.log(res)
      } catch (error) {
        this.message = "error occured : " + error.message
        console.log('error!')
        console.log(error)
      }
      this.isProcessing = false
    },

    async onProcess() {
      this.isProcessing = true
      try {
        const inputdata = {
          //owner: this.$auth_get_user_id(),
          calendarId: "calendar-id",
          content: this.title
        }
        console.log(inputdata)
        const res = await API.graphql(graphqlOperation(processYoteiasobi, inputdata))
        console.log('process done!')
        console.log(res)
      } catch (error) {
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
