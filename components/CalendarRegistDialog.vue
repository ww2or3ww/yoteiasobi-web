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
    </v-toolbar>

    <v-divider></v-divider>
    <section style="margin: 24px;">
      <SelectableAvatarImage
        :propsImageSrc="picture"
        :callbackSelectedPicture="onSelectedPicture"
        :isTile=true
      />
    </section>
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
    
    <section style="margin-left: 16px;">
      <v-btn
        v-if="isRegistMode"
        dark
        color="primary"
        @click="onClickOK"
        width="160"
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
        width="160"
      >
        <v-icon left>
          mdi-autorenew
        </v-icon>
        Edit
      </v-btn>
    </section>

    <section style="margin-left: 16px;" v-if="!isRegistMode">
      <div style="margin-top: 32px;">
        <v-checkbox
          v-model="isCheckDelete"
          label="Delete Account"
        />
      </div>
      <div style="height: 40px;">
        <v-btn
          color="#F8BBD0"
          @click="onDelete"
          :disabled="isProcessing"
          v-show="isCheckDelete"
          small
        >
          Delete
          <v-icon right dark>mdi-account-off-outline</v-icon>
        </v-btn>
      </div>
    </section>

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
    this.isCheckDelete = false
    this.calendarIdTmp = this.calendarId
    this.titleTmp = this.title
    this.descriptionTmp = this.description
  },
  data() {
    return {
      valid: true,
      picture: "", 
      selectedPicture: null,
      headers: [
        { text: "icon", value: "imageAddress", sortable: false },
        { text: 'calendarId', value: 'calendarId' },
        { text: 'title', value: 'title' },
      ],
      calendarIdTmp: "",
      titleTmp: "",
      descriptionTmp: "",
      isProcessing: false,
      isCheckDelete: false,
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
    onSelectedPicture(file) {
      this.selectedPicture = file
      this.picture = URL.createObjectURL(file)
    },
    async onClickOK() {
      try {
        this.isProcessing = true
        const data = {
          calendarId: this.calendarIdTmp,
          title: this.titleTmp, 
          description: this.descriptionTmp,
          image: "",
        }
        await this.callbackOK(this.isRegistMode, false, data)
        
      } catch (error) {
        console.log(error)
      } finally {
        this.isProcessing = false
      }
    },
    onClickCancel() {
      this.callbackCancel()
    },
    async onDelete() {
      try {
        this.isProcessing = true
        const data = {
          calendarId: this.calendarId,
        }
        await this.callbackOK(this.isRegistMode, true, data)
      } catch (error) {
        console.log(error)
      } finally {
        this.isProcessing = false
      }
    }
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
