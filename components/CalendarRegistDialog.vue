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
          v-if="isRegistMode"
          dark
          color="primary"
          @click="onClickOK"
        >
          <v-icon left>
            mdi-pencil
          </v-icon>
          Regist
        </v-btn>
        <v-btn
          v-else
          dark
          color="primary"
          @click="onClickOK"
        >
          <v-icon left>
            mdi-autorenew
          </v-icon>
          Edit
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-divider></v-divider>
    <v-list
      three-line
    >
      <v-form
        ref="form"
        v-model="valid"
        lazy-validation
      >
        <v-text-field
          v-model="calendarIdTmp"
          label="Calendar ID*"
          :rules="[rules.required]"
          counter="60"
          maxlength="60"
          dense
          :readonly="!isRegistMode"
          class="text_field text-white"
        />
        <v-text-field
          v-model="titleTmp"
          label="Title*"
          :rules="[rules.required]"
          counter="50"
          dense
          class="text_field text-white"
        />
        <v-textarea
          v-model="descriptionTmp"
          label="Description"
          counter="500"
          dense
          class="text_field text-white"
        />
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
    calendarId: {
      type: String
    },
    title: {
      type: String
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
  watch: {
    calendarId (nextValue) {
      this.calendarIdTmp = nextValue
    },
    title (nextValue) {
      this.titleTmp = nextValue
    },
    description (nextValue) {
      this.descriptionTmp = nextValue
    },
    isRegistMode (nextValue) {
      if (nextValue) {
        this.$refs.form.resetValidation()
      }
    }
  },
  mounted () {
    this.isProcessing = false
    this.calendarIdTmp = this.calendarId
    this.titleTmp = this.title
    this.descriptionTmp = this.description
  },
  data() {
    return {
      valid: true,
      headers: [
        { text: "icon", value: "imageAddress", sortable: false },
        { text: 'calendarId', value: 'calendarId' },
        { text: 'title', value: 'title' },
      ],
      calendarIdTmp: "",
      titleTmp: "",
      descriptionTmp: "",
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
    async onClickOK() {
      try {
        this.isProcessing = true
        const data = {
          calendarId: this.calendarId,
          title: this.titleTmp, 
          description: this.descriptionTmp,
          image: "",
        }
        await this.callbackOK(this.isRegistMode, data)
        
      } catch (error) {
        console.log(error)
      } finally {
        this.isProcessing = false
      }
    },
    onClickCancel() {
      this.callbackCancel()
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
