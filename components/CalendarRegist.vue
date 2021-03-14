<template>
  <div class="main">
    <section class="section_form">
        <v-text-field
          label="Calendar ID*"
          v-model="calendarId"
          :rules="[rules.required]"
          counter="60"
          maxlength="60"
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
import { createCalendar, createUserCalendar, processYoteiasobi } from "~/src/graphql/mutations"
export default {
  data() {
    return {
      headers: [
        { text: "icon", value: "imageAddress", sortable: false },
        { text: 'calendarId', value: 'calendarId' },
        { text: 'title', value: 'title' },
      ],
      calendarId: "",
      title: "",
      description: "",
      address: "",
      tel: "",
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
  methods: {
    async onRegist() {
      this.isProcessing = true
      try {
        const inputdata = {
          calendarId: this.calendarId,
          title: this.title, 
          description: this.description,
          image: "",
        }
        await API.graphql(graphqlOperation(createCalendar, {input: inputdata}))
        
        const inputuserdata = {
          owner: this.$auth_get_user_id(),
          calendarId: this.calendarId,
          creator: this.$auth_get_user_id(),
        }
        await API.graphql(graphqlOperation(createUserCalendar, {input: inputuserdata}))
        
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
