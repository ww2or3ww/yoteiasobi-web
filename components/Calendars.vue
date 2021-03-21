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
      @click="onClickPlus"
    >
      <v-icon color="white">mdi-plus</v-icon>
    </v-btn>
    <v-dialog
      v-model="isFormShow"
      fullscreen
      transition="dialog-bottom-transition"
    >
      <CalendarRegistDialog
        :formTitle = "formTitle"
        :isRegistMode = "isFormRegistMode"
        :callbackOK = "onFormOK"
        :callbackCancel = "onFormCancel"
        :calendarId = "calendarIdTmp"
        :title = "titleTmp"
        :description = "descriptionTmp"
        :image = "imageTmp"
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
      calendars: null,
      selectedItem: null,
      calendarId: "",
      isFormShow: false,
      isFormRegistMode: false,
      formTitle: "",
      calendarIdTmp: "",
      titleTmp: "",
      descriptionTmp: "",
      imageTmp: "",
    }
  },
  mounted () {
    this.initialize()
  },
  methods: {
    async initialize() {
      this.isFormShow = false
      this.calendars = await this.getItems()
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
          //console.log("---")
          //console.log(data[i])
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
    
    onClickDetail() {
      this.$router.push('/calendars/' + this.calendarId)
    },
    
    onClickEdit() {
      console.log(this.selectedItem)
      this.formTitle = "Edit Calendar"
      this.isFormRegistMode = false
      this.calendarIdTmp = this.selectedItem["calendarId"]
      this.titleTmp = this.selectedItem["title"]
      this.descriptionTmp = this.selectedItem["description"]
      this.imageTmp = this.selectedItem["imageAddress"]
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
    },
    async onFormOK (isRegistMode, isDelete, data) {
      if (isRegistMode) {
        if (data["image"]) {
          data = await this.processImage(data)
        }
        await API.graphql(graphqlOperation(createCalendar, {input: data}))
        const userCalendar = {
          owner: this.$auth_get_user_id(),
          calendarId: data["calendarId"],
          creator: this.$auth_get_user_id(),
        }
        await API.graphql(graphqlOperation(createUserCalendar, {input: userCalendar}))
      } else {
        if (isDelete) {
          const userCalendar = {
            owner: this.$auth_get_user_id(),
            calendarId: data["calendarId"],
          }
          console.log(data)
          console.log(userCalendar)
          console.log(this.selectedItem["image"])
          await Storage.remove(this.selectedItem["image"].replace('public/', ''))
          await API.graphql(graphqlOperation(deleteUserCalendar, {input: userCalendar}))
          await API.graphql(graphqlOperation(deleteCalendar, {input: data}))
        } else {
          await API.graphql(graphqlOperation(updateCalendar, {input: data}))
        }
      }
      this.calendars = await this.getItems()
      this.isFormShow = false
    },
    async processImage(data) {
      if (!data["image"]) {
        return data
      }
      try {
        const selectedPicture = data["image"]
        const pictureKey = this.$auth_create_picture_key(selectedPicture.name, "calendar")
        await this.processUploadFile(pictureKey, selectedPicture)
        data["image"] = pictureKey
      } catch (error) {
        console.log(error)
        data["image"] = ""
      } finally {
        this.isProcessing = false
      }
      return data
    },
    async processUploadFile(pictureKey, selectedPicture) {
      const src = await imageResize.pFileReader(selectedPicture);
      const img = await imageResize.pImage(src);
      const resizedImg = await imageResize.resizeImage(img, 400, 'image/png');
      await Storage.put(pictureKey.replace('public/', ''), resizedImg, {
          level: 'public'
      })
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
