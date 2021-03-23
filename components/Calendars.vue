<template>
  <div class="main">
    <section class="section_list">
      <v-card-title>
        <v-text-field
          v-model="calendarId"
          label="Calendar ID"
          maxlength="60"
        >
          <template v-slot:append>
            <v-btn @click="onClickEdit" :disabled="!isEnableEdit()">
              <v-icon>mdi-square-edit-outline</v-icon>
            </v-btn>
            <v-btn @click="onClickDetail" :disabled="calendarId.length == 0">
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
        <template v-slot:item.imageAddress="{ item }">
          <v-avatar tile>
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
    
    <v-btn fixed fab bottom right 
      color="#BDBDBD88" style="bottom: 40px"
      v-if="isAuthed"
      @click="onClickPlus"
    >
      <v-icon color="white">mdi-plus</v-icon>
    </v-btn>
    <v-dialog
      v-model="isFormShow"
      fullscreen
      transition="dialog-bottom-transition"
      @keydown.esc="onFormCancel"
    >
      <CalendarRegistDialog
        :formTitle = "formTitle"
        :isRegistMode = "isFormRegistMode"
        :callbackOK = "onFormOK"
        :callbackCancel = "onFormCancel"
        :calendarId = "calendarIdTmp"
        :title = "titleTmp"
        :description = "descriptionTmp"
        :imageAddress = "imageAddressTmp"
        :isShow = "isFormShow"
      />
    </v-dialog>
    
  </div>
</template>
<script>
import { API, Storage, graphqlOperation } from 'aws-amplify'
import { createCalendar, createUserCalendar, updateCalendar, deleteCalendar, deleteUserCalendar } from "~/src/graphql/mutations"
import { listUserCalendar, getCalendar } from '~/src/graphql/queries'
import CalendarRegistDialog from '~/components/CalendarRegistDialog'
import imageResize from '~/static/imageResize.js'
export default {
  components: {
    CalendarRegistDialog
  },
  data() {
    return {
      headers: [
        { text: "Icon",         value: "imageAddress",  width: "50px",  sortable: false },
        { text: 'Calendar ID',  value: 'calendarId',    width: "200px" },
        { text: 'Title',        value: 'title' },
      ],
      isAuthed: false,
      calendars: null,
      selectedItem: null,
      calendarId: "",
      isFormShow: false,
      isFormRegistMode: false,
      formTitle: "",
      calendarIdTmp: "",
      titleTmp: "",
      descriptionTmp: "",
      imageAddressTmp: "",
    }
  },
  mounted () {
    this.initialize()
  },
  methods: {
    async initialize() {
      this.isFormShow = false
      this.isAuthed = this.$auth_is_authed()
      if (this.isAuthed) {
        this.calendars = await this.getItems()
      } else {
        this.calendars = []
      }
    },
    async getItems() {
      const owner = this.$auth_get_user_id()
      try {
        const userCalendars = await API.graphql(graphqlOperation(listUserCalendar, {
          owner: owner,
          //calendarId: {
          //  beginsWith: "calendar"
          //},
          limit: 5
        }))
        const data = userCalendars.data.listUserCalendar.items
        console.log(data)
        for(let i = 0; i < data.length; i++) {
          const calendar = await API.graphql(graphqlOperation(getCalendar, {
            calendarId: data[i]["calendarId"]
          }))
          if (calendar.data.getCalendar) {
            data[i]["title"] = calendar.data.getCalendar["title"]
            data[i]["description"] = calendar.data.getCalendar["description"]
            data[i]["image"] = calendar.data.getCalendar["image"]
            data[i]["imageAddress"] = await this.$auth_get_picture_address_from_storage(calendar.data.getCalendar)
          }
        }
        
        return data
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
    
    isEnableEdit() {
      if (!this.selectedItem) {
        return false
      }
      return this.selectedItem["calendarId"] == this.calendarId
    },
    
    clearData() {
      this.selectedItem = null
      this.formTitle = ""
      this.isFormRegistMode = false
      this.calendarIdTmp = ""
      this.titleTmp = ""
      this.descriptionTmp = ""
      this.imageAddressTmp = ""
      this.isFormShow = false
    },
    
    onClickDetail() {
      this.$router.push('/calendars/' + this.calendarId)
    },
    
    onClickEdit() {
      this.formTitle = "Edit Calendar"
      this.isFormRegistMode = false
      this.calendarIdTmp = this.selectedItem["calendarId"]
      this.titleTmp = this.selectedItem["title"]
      this.descriptionTmp = this.selectedItem["description"]
      this.imageAddressTmp = this.selectedItem["imageAddress"]
      this.isFormShow = true
    },
    
    onClickPlus() {
      this.formTitle = "Regist Calendar"
      this.isFormRegistMode = true
      this.calendarIdTmp = ""
      this.titleTmp = ""
      this.descriptionTmp = ""
      this.isFormShow = true
    },
    
    onFormCancel () {
      this.isFormShow = false
      this.clearData()
    },
    
    async onFormOK (isRegistMode, isDelete, data) {
      if (data["selectedImage"]) {
        const imageKey = await this.processImage(data["selectedImage"], data["calendarId"])
        data["image"] = imageKey
      }
      delete data["selectedImage"]
      if (isRegistMode) {
        const userCalendar = {
          owner: this.$auth_get_user_id(),
          calendarId: data["calendarId"],
          creator: this.$auth_get_user_id(),
        }
        await API.graphql(graphqlOperation(createCalendar, {input: data}))
        await API.graphql(graphqlOperation(createUserCalendar, {input: userCalendar}))
      } else {
        if (isDelete) {
          const userCalendar = {
            owner: this.$auth_get_user_id(),
            calendarId: data["calendarId"],
          }
          if (this.selectedItem["image"]) {
            await Storage.remove(this.selectedItem["image"].replace('public/', ''))
          }
          await API.graphql(graphqlOperation(deleteUserCalendar, {input: userCalendar}))
          await API.graphql(graphqlOperation(deleteCalendar, {input: data}))
        } else {
          await API.graphql(graphqlOperation(updateCalendar, {input: data}))
        }
      }
      this.calendars = await this.getItems()
      this.isFormShow = false
      this.clearData()
    },
    async processImage(selectedImage, calendarId) {
      try {
        const filename = selectedImage.name
        const ext = filename.slice(filename.lastIndexOf('.') + 1)
        const imageKey = "public/calendar/" + this.$auth_get_user_id() + "/" + calendarId + "." + ext
        await Storage.remove(imageKey.replace('public/', ''))
        const src = await imageResize.pFileReader(selectedImage);
        const img = await imageResize.pImage(src);
        const resizedImg = await imageResize.resizeImage(img, 400, 'image/png');
        await Storage.put(imageKey.replace('public/', ''), resizedImg, {
            level: 'public'
        })
        return imageKey
      } catch (error) {
        console.log(error)
      }
    },
  }
}
</script>
<style>
.section_list {
  margin: 4px;
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
