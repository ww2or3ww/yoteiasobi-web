<template>
  <div class="main">
    <v-sheet>
      <v-toolbar-title
        style="margin-left: 4px;"
        v-if="$refs.calendar"
      >
        {{ calendarTitle }}
      </v-toolbar-title>
      <v-toolbar-title
        style="margin-left: 4px;"
        v-if="$refs.calendar"
      >
        {{ $refs.calendar.title }}
      </v-toolbar-title>
    </v-sheet>
    <v-sheet>
      <v-toolbar flat>
        <v-btn
          outlined
          style="margin-right:8px;"
          @click="setToday"
        >
          <v-icon left>mdi-calendar-today</v-icon>
          Today
        </v-btn>
        <v-btn
          fab
          small
          style="margin-right:8px;"
          @click="$refs.calendar.prev()"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
        <v-btn
          fab
          small
          style="margin-right:8px;"
          @click="$refs.calendar.next()"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
        <v-spacer></v-spacer>
        <v-menu
          bottom
          right
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              outlined
              v-bind="attrs"
              v-on="on"
            >
              <span>{{ typeToLabel[type] }}</span>
              <v-icon right>
                mdi-menu-down
              </v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="type = 'day'">
              <v-list-item-title>Day</v-list-item-title>
            </v-list-item>
            <v-list-item @click="type = 'week'">
              <v-list-item-title>Week</v-list-item-title>
            </v-list-item>
            <v-list-item @click="type = 'month'">
              <v-list-item-title>Month</v-list-item-title>
            </v-list-item>
            <v-list-item @click="type = '4day'">
              <v-list-item-title>4days</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar>
    </v-sheet>
    <v-sheet :height="calendarHeight">
      <v-calendar
        ref="calendar"
        v-model="focus"
        :now="focus"
        :weekdays="weekday"
        :type="type"
        :events="events"
        :event-color="getEventColor"
        @click:event="onClickEvent"
        @click:more="onClickDate"
        @click:date="onClickDate"
        color="primary"
      ></v-calendar>
    </v-sheet>
    
    <v-btn fixed fab bottom right 
      v-if="isAuthed"
      color="#BDBDBD88" style="bottom: 40px"
      @click="onClickPlus"
    >
      <v-icon color="white">mdi-plus</v-icon>
    </v-btn>
    
    <v-dialog
      v-model="isShowForm"
      fullscreen
      transition="dialog-bottom-transition"
    >
      <CalendarEventRegistDialog
        :formTitle = "formTitle"
        :isRegistMode = "isFormRegistMode"
        :isMasked = "isMasked"
        :isMine = "isMine"
        :calendarId = "calendarId"
        :name = "name"
        :dateStart = "dateStart"
        :dateEnd = "dateEnd"
        :timeStart = "timeStart"
        :timeEnd = "timeEnd"
        :selectedDate = "selectedDate"
        :email = "email"
        :description = "description"
        :scopeLv = "scopeLv"
        :callbackOK = "onFormOK"
        :callbackCancel = "onFormCancel"
        :isShow = "isShowForm"
      />
    </v-dialog>
    
    <v-dialog v-model="isShowMessage" width="480">
      <MessageBox
        :callbackBtn="onMessageClose"
        :text="message"
        :isShowCancel="false"
      />
    </v-dialog>

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
import { getCalendar } from '~/src/graphql/queries'
import SelectableAvatarImage from '~/components/SelectableAvatarImage.vue'
import CalendarEventRegistDialog from '~/components/CalendarEventRegistDialog.vue'
import MessageBox from '~/components/MessageBox.vue'
export default {
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isAuthed: false,
      calendarId: "",
      calendarTitle: "",
      calendarOwner: "",
      formTitle: "",
      isFormRegistMode: false,
      isMasked: false,
      isMine: false,
      name: "",
      dateStart: "",
      dateEnd: "",
      timeStart: "",
      timeEnd: "",
      email: "",
      description: "",
      scopeLv: "Private",
      isProcessing: false,
      isShowForm: false,
      isShowMessage: false,
      message: "",
      
      type: 'month',
      types: ['month', 'week', 'day', '4day'],
      typeToLabel: {
        month: 'MONTH',
        week: 'WEEK',
        day: 'DAY',
        '4day': '4DAYS',
      },
      weekday: [0, 1, 2, 3, 4, 5, 6],
      weekdays: [
        { text: 'Sun - Sat', value: [0, 1, 2, 3, 4, 5, 6] },
        { text: 'Mon - Sun', value: [1, 2, 3, 4, 5, 6, 0] },
        { text: 'Mon - Fri', value: [1, 2, 3, 4, 5] },
        { text: 'Mon, Wed, Fri', value: [1, 3, 5] },
      ],
      focus: null,
      selectedDate: '',
      events: [],
      calendarHeight: 600,
    }
  },
  mounted () {
    this.calendarId = this.id
    this.email = this.$auth_get_email()
    this.focus = this.convertToDate(new Date())
    this.initialize()
  },
  created() {
    window.addEventListener('resize', this.onResize)
    this.onResize()
  },
  destroyed() {
    window.removeEventListener('resize', this.onResize)
  },
  methods: {
    async initialize() {
      let isSuccessGetData = false
      
      try {
        this.isProcessing = true
        this.isAuthed = this.$auth_is_authed()
        this.isShowForm = false
        this.setToday()
        if (this.calendarId) {
          const retItems = await this.getItem()
          if (retItems) {
            this.events = retItems
            isSuccessGetData = true
          }
        }
        
        const calendar = await API.graphql(graphqlOperation(getCalendar, {
          calendarId: this.calendarId
        }))
        if (calendar.data.getCalendar) {
          this.calendarTitle = calendar.data.getCalendar["title"]
          this.calendarOwner = calendar.data.getCalendar["owner"]
        }
      } catch (error) {
        console.log(error)
      } finally {
        this.isProcessing = false
      }

      if (!isSuccessGetData) {
        this.isShowMessage = true
        if (this.calendarOwner == this.$auth_get_user_id()) {
          this.message = "Failed to retrieve calendar data.\nPlease share your calendar with the following service accounts.\n"
          this.message = this.message + process.env.ENVVAL_GCP_SERVICE_ACCOUNT
        } else {
          this.message = "Failed to retrieve calendar data.\nPlease contact the calendar owner."
        }
      }
    },
    onResize() {
      this.calendarHeight = window.innerHeight - 280
    },
    onMessageClose() {
      this.isShowMessage = false
    },
    async getItem() {
      try {
        const calendar = await API.get(
          process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
          '/calendar/' + this.calendarId
        )
        calendar.forEach(function(data){
          data.start = new Date(data.start)
          data.end = new Date(data.end)
        })
        return calendar
      } catch (error) {
        console.log(error)
        return null
      }
    },
    getEventColor (event) {
      if (event['isMasked']) {
        return '#757575'
      } else if (event['isMine']) {
        return 'orange'
      } else if (event['isProtected']) {
        return 'green'
      } else if (event['isPublic']) {
        return 'blue'
      }
      return '#455A64'
    },
    setToday () {
      this.focus = this.$moment().format('YYYY-MM-DD')
      this.selectedDate = this.focus
    },
    onClickDate (data) {
      if(this.selectedDate == data["date"]) {
        this.type = 'day'
      }
      this.focus = data["date"]
      this.selectedDate = this.focus
    },
    convertToDate (date) {
      return date.getFullYear() + "-" + 
        ("00" + (date.getMonth() + 1)).slice(-2) + "-" + 
        ("00" + date.getDate()).slice(-2)
    },
    convertToTime (date) {
      return ("00" + date.getHours()).slice(-2) + ":" + 
        ("00" + date.getMinutes()).slice(-2)
    },
    onClickEvent (data) {
      console.log(data)
      const event = data["event"]
      const dateStart = new Date(event["start"])
      const dateEnd = new Date(event["end"])

      this.name = event["name"]
      this.description = event["description"]
      this.isMasked = event["isMasked"]
      this.isMine = event['isMine']
      this.dateStart = this.convertToDate(dateStart)
      this.dateEnd = this.convertToDate(dateEnd)
      this.timeStart = this.convertToTime(dateStart)
      this.timeEnd = this.convertToTime(dateEnd)
      
      if(event["isProtected"]) {
        this.scopeLv = "Protected"
      } else if(event["isPublic"]) {
        this.scopeLv = "Public"
      } else {
        this.scopeLv = "Private"
      }

      this.formTitle = "Event Information"
      this.isFormRegistMode = false
      this.isShowForm = true
    },
    onClickPlus () {
      this.dateStart = this.focus
      this.dateEnd = this.focus
      
      const dateNow = new Date()
      dateNow.setMinutes(0)
      this.timeStart = this.convertToTime(dateNow)
      this.timeEnd = this.convertToTime(dateNow)
      this.isMasked = false
      this.isMine = true
      this.scopeLv = "Private"
      this.formTitle = "Event Registration"
      this.isFormRegistMode = true
      this.isShowForm = true
    },
    async onFormOK (data) {
      const postdata = {
        headers: {},
        body: data,
        response: true,
      };
      const response = await API.post(
        process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
        '/calendar',
        postdata
      )
      this.events.push(data)
      this.isShowForm = false
    },
    onFormCancel () {
      this.isShowForm = false
    }
  },
}
</script>
<style>
.section_avatar {
  text-align: center;
  margin: 24px;
}
.section_form {
  margin-bottom: 32px;
}
.outlined {
    border: 4px solid #00F;
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
