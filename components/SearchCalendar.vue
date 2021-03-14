<template>
  <div class="main">
    <section class="section_list">
      <v-card-title>
        <v-text-field
          v-model="calendarId"
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
import { listPrivateNotes } from '~/src/graphql/queries'
import { createPrivateNote } from "~/src/graphql/mutations"
export default {
  data() {
    return {
      headers: [
        { text: "icon", value: "imageAddress", sortable: false },
        { text: 'id', value: 'id' },
        { text: 'owner', value: 'owner' },
        { text: 'content', value: 'content' },
      ],
      calendarId: "",
      privateNotes: null,
      isProcessing: false,
      message: "",
    }
  },
  mounted () {
    this.initialize()
  },
  methods: {
    async initialize() {
    },
    async getItems() {
      try {
        let privateNotes = await API.graphql(graphqlOperation(
          listPrivateNotes, {limit: 10}
        ))
        console.log(privateNotes)
        return privateNotes.data.listPrivateNotes.items
      } catch (error) {
        console.log(error)
        this.users = null
      }
    },
    async onClickSearch() {
      this.$router.push('/calendar?id=' + this.calendarId)
    },
    onRegist() {
      this.registProcess()
    },
    async registProcess() {
      this.isProcessing = true
      try {
        const privateNote = {content: this.comment}
        await API.graphql(graphqlOperation(createPrivateNote, {input: privateNote}))
      } catch (error) {
        this.isProcessing = false
        this.message = "error occured : " + error.message
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
