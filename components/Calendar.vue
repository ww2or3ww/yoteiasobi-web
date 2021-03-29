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
        :weekdays="weekday"
        :type="type"
        :events="events"
        :event-color="getEventColor"
        @click:date="viewDay"
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
        formTitle = "Regist Event"
        :calendarId = "calendarId"
        :name = "name"
        :dateStart = "dateStart"
        :dateEnd = "dateEnd"
        :timeStart = "timeStart"
        :timeEnd = "timeEnd"
        :selectedDate = "focus"
        :email = "email"
        :description = "description"
        :callbackOK = "onFormOK"
        :callbackCancel = "onFormCancel"
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
import { API } from 'aws-amplify'
import SelectableAvatarImage from '~/components/SelectableAvatarImage.vue'
import CalendarEventRegistDialog from '~/components/CalendarEventRegistDialog.vue'
export default {
  components: {
    SelectableAvatarImage,
    CalendarEventRegistDialog
  },
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
      name: "",
      dateStart: "",
      dateEnd: "",
      timeStart: "",
      timeEnd: "",
      email: "",
      description: "",
      isProcessing: false,
      isShowForm: false,
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
      focus: '',
      events: [],
      calendarHeight: 600,
    }
  },
  mounted () {
    this.calendarId = this.id
    this.calendarTitle = "calendar for me"
    this.email = this.$auth_get_email()
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
      this.isAuthed = this.$auth_is_authed()
      this.isShowForm = false
      this.setToday()
      if (this.calendarId && this.calendarId.length > 10) {
        this.isProcessing = true
        this.events= await this.getItem()
        this.isProcessing = false
      }
    },
    onResize() {
      this.calendarHeight = window.innerHeight - 280
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
      }
    },
    setToday () {
      this.focus = this.$moment().format('YYYY-MM-DD')
    },
    viewDay ({ date }) {
      this.focus = date
      this.type = 'day'
      console.log(this.focus)
    },
    getEventColor (event) {
      if (event['isMasked']) {
        return '#757575'
      } else if (event['isMine']) {
        return 'orange'
      }
      return '#455A64'
    },
    onClickPlus () {
      this.dateStart = this.focus
      this.dateEnd = this.focus
      this.timeStart = '00:00'
      this.timeEnd = '00:00'
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
