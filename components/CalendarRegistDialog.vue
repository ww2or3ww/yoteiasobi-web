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
    <section style="margin: 24px 24px 4px 24px;">
      <SelectableAvatarImage
        :propsImageSrc="imageAddressTmp"
        :callbackSelectedPicture="onSelectedPicture"
        :isTile=true
        :readonly="!isOwnItem"
      />
    </section>
    <v-list>
      <v-form
        v-model="isFormValid"
        ref="form"
        lazy-validation
      >
        <v-text-field
          v-model="calendarIdTmp"
          label="Calendar ID*"
          :rules="[rules.required, rules.minimum(calendarIdTmp, 12, 'characters'), rules.mail]"
          counter="60"
          maxlength="60"
          dense
          :readonly="!isRegistMode || !isOwnItem"
          class="text_field text-white"
        />
        <v-text-field
          v-model="titleTmp"
          label="Title*"
          :rules="[rules.required, rules.minimum(titleTmp, 5, 'characters')]"
          counter="30"
          maxlength="30"
          dense
          :readonly="!isOwnItem"
          class="text_field text-white"
        />
        <v-textarea
          v-model="descriptionTmp"
          label="Description"
          counter="300"
          maxlength="300"
          rows="3"
          dense
          :readonly="!isOwnItem"
          class="text_field text-white"
        />
      </v-form>

    </v-list>
    
    <v-card v-show="isOwnItem">
      <v-card-text style="padding-top: 0;">
        <p style="margin: 0;">
          登録したカレンダーの、
        </p>
        <p style="margin: 0;">
          [ カレンダーの設定 > 特定のユーザーとの共有] へ 
        </p>
        <p style="margin: 0;">
          以下のサービスアカウントを追加してください。
        </p>
        <p style="margin: 0;">
          (「変更および共有の管理権限」としてください)
        </p>
        <p style="margin: 8px 0 8px 0;">
          {{ serviceAccount }}
        </p>
      </v-card-text>
    </v-card>
    
    <section style="margin-left: 16px;">
      <v-btn
        v-if="isRegistMode"
        :disabled="!isFormValid"
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
        v-show="isOwnItem"
        :disabled="!isFormValid"
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

    <section style="margin-left: 16px;" v-if="!isRegistMode" v-show="isOwnItem">
      <div style="margin-top: 32px;">
        <v-checkbox
          v-model="isCheckDelete"
          label="Delete Calendar"
        />
      </div>
      <div style="height: 40px;">
        <v-btn
          color="#FF6666"
          @click="onDelete"
          :disabled="isProcessing"
          v-show="isCheckDelete"
          small
        >
          Delete
          <v-icon right dark>mdi-delete-forever</v-icon>
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

    <v-dialog v-model="isShowMessage" width="480">
      <MessageBox
        :callbackBtn="processDelete"
        :text="message"
      />
    </v-dialog>
    
  </v-card>
</template>
<script>
import MessageBox from '~/components/MessageBox.vue'
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
    isOwnItem: {
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
    imageAddress: {
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
      this.isCheckDelete = false
      if (this.isRegistMode) {
        this.calendarIdTmp = ""
        this.titleTmp = ""
        this.descriptionTmp = ""
        this.imageAddressTmp = ""
      }
      this.$refs.form.validate()
    },
    calendarId (nextValue) {
      this.calendarIdTmp = nextValue
    },
    title (nextValue) {
      this.titleTmp = nextValue
    },
    description (nextValue) {
      this.descriptionTmp = nextValue
    },
    imageAddress (nextValue) {
      this.imageAddressTmp = nextValue
    },
  },
  mounted () {
    this.isProcessing = false
    this.isCheckDelete = false
    this.calendarIdTmp = this.calendarId
    this.titleTmp = this.title
    this.descriptionTmp = this.description
    this.imageAddressTmp = this.imageAddress
    this.$refs.form.validate()
    this.serviceAccount = process.env.ENVVAL_GCP_SERVICE_ACCOUNT
  },
  data() {
    return {
      serviceAccount: "",
      isFormValid: false,
      imageAddressTmp: "", 
      selectedImage: null,
      calendarIdTmp: "",
      titleTmp: "",
      descriptionTmp: "",
      isProcessing: false,
      isCheckDelete: false,
      isShowMessage: false,
      message: "",
      rules: {
        required: value => !!value || 'Required.',
        tel: value => {
          const pattern = /^[0-9]{10,11}$/
          return (value.length == 0 || pattern.test(value)) || 'Invalid TEL.'
        },
        mail: value => {
          const pattern = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@{1}[A-Za-z0-9_.-]{1,}\.[A-Za-z0-9]{1,}$/
          return (value.length == 0 || pattern.test(value)) || 'Invalid Value.'
        },
        minimum (value, min, unit) {
          return value.length >= min || "Too small (Need more " + min + " " + unit + ")"
        }
      }
    }
  },
  methods: {
    onSelectedPicture(file) {
      this.selectedImage = file
      this.imageAddressTmp = URL.createObjectURL(file)
    },
    async onClickOK() {
      try {
        const isDelete = false
        this.isProcessing = true
        const data = {
          calendarId: this.calendarIdTmp,
          title: this.titleTmp, 
          description: this.descriptionTmp,
          selectedImage: this.selectedImage
        }
        await this.callbackOK(this.isRegistMode, isDelete, data)
        
      } catch (error) {
        console.log(error)
      } finally {
        this.isProcessing = false
      }
    },
    onClickCancel() {
      this.callbackCancel()
    },
    onDelete() {
      this.message = "Delete your calendar. Are you sure ?"
      this.isShowMessage = true
    },
    async processDelete(typestr) {
      this.isShowMessage = false
      if (typestr == "cancel") {
        return
      }
      this.isProcessing = true
      try {
        const isDelete = true
        const data = {
          calendarId: this.calendarId,
        }
        await this.callbackOK(this.isRegistMode, isDelete, data)
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
