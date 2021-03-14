<template>
  <v-container style="padding: 0;">
    <v-row>
      <v-col>
        <v-dialog
          v-model="isShowDatePicker"
          width="280px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="dateSet"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="dateTmp"
            scrollable
          >
            <v-spacer></v-spacer>
            <v-btn
              text
              color="primary"
              @click="onClickCancelDate"
            >
              Cancel
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="onClickOKDate"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-dialog>
      </v-col>
      <v-col>
        <v-dialog
          v-model="isShowTimePicker"
          width="280px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="timeSet"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-time-picker
            v-if="isShowTimePicker"
            v-model="timeTmp"
            full-width
            :allowed-minutes="allowedStep"
            format="24hr"
          >
            <v-spacer></v-spacer>
            <v-btn
              text
              color="primary"
              @click="onClickCancelTime"
            >
              Cancel
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="onClickOKTime"
            >
              OK
            </v-btn>
          </v-time-picker>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  props: {
    time: {
      type: String,
      required: true
    },
    date: {
      type: String,
      required: true
    },
    callbackOK: {
      type: Function, 
      required: true
    },
  },
  watch: {
    time (nextValue) {
      this.timeSet = nextValue
      this.timeTmp = nextValue
    },
    date (nextValue) {
      this.dateSet = nextValue
      this.dateTmp = nextValue
    }
  },
  data() {
    return {
      isShowDatePicker: false,
      isShowTimePicker: false,
      dateSet: "",
      dateTmp: "",
      timeSet: "",
      timeTmp: "",
    }
  },
  mounted () {
    this.isShowDatePicker = false
    this.isShowTimePicker = false
    this.dateSet = this.date
    this.dateTmp = this.date
    this.timeSet = this.time
    this.timeTmp = this.time
  },
  methods: {
    onClickCancelDate() {
      this.isShowDatePicker=false
      this.dateTmp = this.dateSet
    },
    onClickOKDate() {
      this.isShowDatePicker=false
      this.dateSet = this.dateTmp
      this.callbackOK(this.dateSet, this.timeSet)
    },
    onClickCancelTime() {
      this.isShowTimePicker=false
      this.timeTmp = this.timeSet
    },
    onClickOKTime() {
      this.isShowTimePicker=false
      this.timeSet = this.timeTmp
      this.callbackOK(this.dateSet, this.timeSet)
    },
    allowedStep(m) {
      return m % 10 === 0
    },
  },
}
</script>
