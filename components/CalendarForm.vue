<template>
  <v-card>
    <v-toolbar>
      <v-btn
        icon
        dark
        @click="onClickCancel"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-toolbar-title>
        {{ formTitle }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn
          dark
          color="primary"
          @click="onClickOK"
        >
          <v-icon left>
            mdi-pencil
          </v-icon>
          Save
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-divider></v-divider>
    <v-list
      three-line
    >
      <v-subheader>{{ selectedDate }}</v-subheader>
      <v-list-item>
        <v-list-item-action>
          <v-icon>
            mdi-subtitles-outline
          </v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-text-field
            v-model="nameTmp"
            dense
            :rules="[rules.required]"
          />
        </v-list-item-content>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-action>
          <v-icon>
            mdi-email
          </v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-text-field
            v-model="email"
            readonly
            dense
          />
        </v-list-item-content>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-action>
          <v-icon>
            mdi-clock-time-five-outline
          </v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <CalendarDatePickerDialog
            :date="dateStartTmp"
            :time="timeStartTmp"
            :callbackOK="onCallbackOKStart"
          />
          <CalendarDatePickerDialog
            :date="dateEndTmp"
            :time="timeEndTmp"
            :callbackOK="onCallbackOKEnd"
          />
        </v-list-item-content>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-action>
          <v-icon>
            mdi-pencil
          </v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-textarea
            v-model="descriptionTmp"
            maxlength="500"
            counter="500"
            dense
          />
        </v-list-item-content>
      </v-list-item>
      
    </v-list>
  </v-card>
</template>

<script>
import CalendarDatePickerDialog from '~/components/CalendarDatePickerDialog.vue'
export default {
  props: {
    formTitle: {
      type: String,
      required: true
    },
    selectedDate: {
      type: String,
      required: true
    },
    calendarId: {
      type: String
    },
    name: {
      type: String
    },
    dateStart: {
      type: String
    },
    dateEnd: {
      type: String
    },
    timeStart: {
      type: String
    },
    timeEnd: {
      type: String
    },
    email: {
      type: String, 
      required: true
    },
    description: {
      type: String
    },
    callbackOK: {
      type: Function, 
      required: true
    },
    callbackCancel: {
      type: Function, 
      required: true
    },
  },
  data() {
    return {
      isShowTimeStart: false,
      nameTmp: "",
      dateStartTmp: "",
      dateEndTmp:"",
      timeStartTmp: "",
      timeEndTmp: "",
      descriptionTmp: "",
      rules: {
        required: value => !!value || 'Required.',
      }
    }
  },
  mounted () {
    this.isShowTimeStart = false
    this.nameTmp = this.name
    this.dateStartTmp = this.dateStart
    this.dateEndTmp = this.dateEnd
    this.timeStartTmp = this.timeStart
    this.timeEndTmp = this.timeEnd
    this.descriptionTmp = this.description
  },
  methods: {
    onCallbackOKStart(date, time) {
      this.dateStartTmp = date
      this.timeStartTmp = time
    },
    onCallbackOKEnd(date, time) {
      this.dateEndTmp = date
      this.timeEndTmp = time
    },
    onClickOK() {
      const data = {
        "calendarId": this.calendarId,
        "name": this.nameTmp,
        "start": new Date(this.$moment(this.dateStartTmp + 'T' + this.timeStartTmp).format('YYYY-MM-DDTHH:mm')),
        "end": new Date(this.$moment(this.dateEndTmp + 'T' + this.timeEndTmp).format('YYYY-MM-DDTHH:mm')),
        "description": this.descriptionTmp,
        "timed": true,
      }
      this.callbackOK(data)
    },
    onClickCancel() {
      this.callbackCancel()
    },
  },
}
</script>
