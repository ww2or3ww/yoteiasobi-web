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
      <v-toolbar-items v-show="isRegistMode">
        <v-btn
          dark
          color="primary"
          @click="onClickOK"
          :disabled="!isFormValid"
        >
          <v-icon left>
            mdi-pencil
          </v-icon>
          Regist
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-divider></v-divider>
    <v-list
      three-line
    >
      <v-subheader>{{ selectedDate }}</v-subheader>
      
      <v-form
        v-model="isFormValid"
        ref="form"
        lazy-validation
      >
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
              :rules="[rules.required, rules.minimum(nameTmp, 3, 'characters')]"
              counter="50"
              maxlength="50"
              :readonly="!isRegistMode"
            />
          </v-list-item-content>
        </v-list-item>
        
        <v-list-item v-show="isRegistMode">
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
            <v-card-text style="margin:0; padding:0;">
              <p style="margin:0; padding:0;">※カレンダーオーナーにEmailが共有されます。</p>
            </v-card-text>
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
              :readonly="!isRegistMode"
            />
            <CalendarDatePickerDialog
              :date="dateEndTmp"
              :time="timeEndTmp"
              :callbackOK="onCallbackOKEnd"
              :readonly="!isRegistMode"
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
              rows="3"
              :readonly="!isRegistMode"
            />
          </v-list-item-content>
        </v-list-item>
      
        <v-list-item v-show="!isMasked">
          <v-list-item-action style="padding-top: 16px;">
            <v-icon>
              mdi-lock-check-outline
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-radio-group
              :readonly="!isMine"
              v-model="scopeLvTmp"
              row
            >
              <v-radio
                label="Private"
                value="Private"
              ></v-radio>
              <v-radio
                label="Protected"
                value="Protected"
              ></v-radio>
              <v-radio
                label="Public"
                value="Public"
              ></v-radio>
            </v-radio-group>
          </v-list-item-content>
        </v-list-item>
    
      </v-form>
      
    </v-list>

    <v-overlay :value="isProcessing">
      <v-progress-circular
        :size="100"
        :width="8"
        color="primary"
        indeterminate
      />
    </v-overlay>

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
    isRegistMode: {
      type: Boolean,
      required: true
    },
    isMasked: {
      type: Boolean
    },
    isMine: {
      type: Boolean
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
    scopeLv: {
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
    isShow: {
      type: Boolean,
    }
  },
  watch: {
    isShow (nextValue) {
      if (this.isRegistMode) {
        this.nameTmp = ""
        this.descriptionTmp = ""
        this.scopeLvTmp = "Private"
      } else {
        this.nameTmp = this.name
        this.descriptionTmp = this.description
        this.scopeLvTmp = this.scopeLv
      }
      this.dateStartTmp = this.dateStart
      this.dateEndTmp = this.dateEnd
      this.timeStartTmp = this.timeStart
      this.timeEndTmp = this.timeEnd
      this.$refs.form.validate()
    },
  },
  data() {
    return {
      isProcessing: false,
      isShowTimeStart: false,
      nameTmp: "",
      dateStartTmp: "",
      dateEndTmp:"",
      timeStartTmp: "",
      timeEndTmp: "",
      descriptionTmp: "",
      scopeLvTmp: "Private",
      isFormValid: false,
      rules: {
        required: value => !!value || 'Required.',
        minimum (value, min, unit) {
          return value.length >= min || "Too small (Need more " + min + " " + unit + ")"
        }
      }
    }
  },
  mounted () {
    this.isProcessing = false
    this.isShowTimeStart = false
    this.nameTmp = this.name
    this.dateStartTmp = this.dateStart
    this.dateEndTmp = this.dateEnd
    this.timeStartTmp = this.timeStart
    this.timeEndTmp = this.timeEnd
    this.descriptionTmp = this.description
    this.scopeLvTmp = this.scopeLv
    this.$refs.form.validate()
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
    async onClickOK() {
      try {
        this.isProcessing = true
        const data = {
          "type": "calendar_event",
          "calendarId": this.calendarId,
          "name": this.nameTmp,
          "start": new Date(this.$moment(this.dateStartTmp + 'T' + this.timeStartTmp).format('YYYY-MM-DDTHH:mm')),
          "end": new Date(this.$moment(this.dateEndTmp + 'T' + this.timeEndTmp).format('YYYY-MM-DDTHH:mm')),
          "description": this.descriptionTmp,
          "timed": true,
        }
        await this.callbackOK(data)
      } catch (error) {
        console.log(error)
      } finally {
        this.isProcessing = false
      }
    },
    onClickCancel() {
      this.callbackCancel()
    },
  },
}
</script>
