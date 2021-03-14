<template>
  <div class="main">
    <section class="section_list">
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
      <v-card-title>
        <v-text-field
          v-model="calendarId"
          label="Calendar ID"
          counter="60"
          maxlength="60"
        >
          <template v-slot:append>
            <v-btn @click="onClickSearch" :disabled="calendarId.length == 0">
              <v-icon>mdi-calendar-month</v-icon>
            </v-btn>
          </template>
        </v-text-field>
      </v-card-title>
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
export default {
  data() {
    return {
      headers: [
        { text: "Icon",         value: "imageAddress",  width: "50px",  sortable: false },
        { text: 'Calendar ID',  value: 'calendarId',    width: "200px" },
        { text: 'Title',        value: 'title' },
      ],
      calendars: null,
      selectedItem: null,
      calendarId: "",
      isProcessing: false,
      message: "",
    }
  },
  mounted () {
    this.initialize()
  },
  methods: {
    async initialize() {
      this.isProcessing = true
      this.calendars = await this.getItems()
      this.isProcessing = false
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
    
    onClickRow(item) {
      console.log(item)
      this.selectedItem = item
      this.calendarId = item["calendarId"]
    },
    
    onClickSearch() {
      this.$router.push('/calendar?id=' + this.calendarId)
    },
    
  }
}
</script>
<style>
.section_list {
  margin: 32px;
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
