<template>
  <div class="main">
    <section class="section_avatar">
      <SelectableAvatarImage
        :propsImageSrc="picture"
        :callbackSelectedPicture="onSelectedPicture"
      />
    </section>
    
    <section class="section_form">
      <v-form v-model="isFormValid">
        <v-text-field
          v-model="name"
          label="Name*"
          :rules="[rules.required]"
          dense
          class="text_field text-white"
        />
        <v-text-field
          v-model="email"
          label="Email*"
          :rules="[rules.required, rules.email]"
          dense
          readonly
          class="text_field text-gray"
        />
        <v-textarea
          v-model="comment"
          label="Comment"
          counter="500"
          dense
          class="text_field text-white"
        />
      </v-form>
    </section>
    
    <section class="section_buttons">
      <v-btn
        color="#607D8B"
        @click="onCancel"
        :disabled="isProcessing || !isEdited()"
      >
        Cancel
        <v-icon right dark>mdi-keyboard-backspace</v-icon>
      </v-btn>
      <v-btn
        color="#607D8B"
        @click="onUpdate"
        :disabled="!isFormValid || isProcessing || !isEdited()"
      >
        Update
        <v-icon right dark>mdi-account-edit-outline</v-icon>
      </v-btn>
    </section>
    <section class="section_buttons">
      <div style="float: right;">
        <v-checkbox
          v-model="isCheckDelete"
          label="Delete Account"
        />
      </div>
      <div style="clear:both; height: 40px;">
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

    <v-dialog v-model="isShowMessage" width="400">
      <MessageBox
        :callbackBtn="processDelete"
        text="Delete your account. Are you sure ?"
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
import { API, Storage } from 'aws-amplify'
import SelectableAvatarImage from '~/components/SelectableAvatarImage.vue'
import MessageBox from '~/components/MessageBox.vue'
import imageResize from '~/static/imageResize.js'
export default {
  components: {
    SelectableAvatarImage,
    MessageBox,
  },
  data() {
    return {
      name: "", 
      name_org: "",
      email: "",
      email_org: "",
      comment: "",
      comment_org: "",
      picture: "", 
      picture_org: "",
      selectedPicture: null,
      isFormValid: false,
      isProcessing: false,
      isCheckDelete: false,
      isShowMessage: false,
      message: "",
      rules: {
        required: value => !!value || 'Required.',
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Invalid e-mail.'
        },
      }
    }
  },
  mounted () {
    this.dataInitialize()
  },
  methods: {
    dataInitialize() {
      this.name = this.$auth_get_name()
      this.email = this.$auth_get_email()
      this.comment = this.$auth_get_comment()
      this.picture = this.$auth_get_picture()
      this.selectedPicture = null
      this.name_org = this.name
      this.email_org = this.email
      this.comment_org = this.comment
      this.picture_org = this.picture
      this.isProcessing = false
    },
    isEdited(){
      return this.name != this.name_org ||
        this.comment != this.comment_org ||
        this.picture != this.picture_org
    },
    onSelectedPicture(file) {
      this.selectedPicture = file
      this.picture = URL.createObjectURL(file)
    },
    onUpdate() {
      this.updateProcess()
    },
    onDelete() {
      this.isShowMessage = true
    },
    onCancel() {
      this.name = this.name_org
      this.comment = this.comment_org
      this.picture = this.picture_org
    },
    async updateProcess() {
      this.isProcessing = true
      try {
        let pictureKey = null
        if (this.selectedPicture) {
          pictureKey = this.$auth_create_picture_key(this.selectedPicture.name)
          await this.processUploadFile(pictureKey)
        }
        await this.processUpdateUser(pictureKey)

        this.$auth_reload_user(this.dataInitialize)
      } catch (error) {
        this.isProcessing = false
        this.message = "error occured : " + error.message
      }
    },
    async processUploadFile(pictureKey) {
      const src = await imageResize.pFileReader(this.selectedPicture);
      const img = await imageResize.pImage(src);
      const resizedImg = await imageResize.resizeImage(img, 400, 'image/png');
      await Storage.put(pictureKey.replace('public/', ''), resizedImg, {
          level: 'public'
      })
    },
    async processUpdateUser(pictureKey) {
      const data = {
        headers: {},
        body: {
          'name': this.name,
          'comment': this.comment,
          'picture': pictureKey
        },
        response: true,
      };
      const response = await API.put(
        process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
        '/profile', 
        data
      )
    },
    async processDelete(typestr) {
      this.isShowMessage = false
      if (typestr == "cancel") {
        return
      }
      this.isProcessing = true
      try {
        const response = await API.del(
          process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
          '/profile/' + this.$auth_get_user_id()
        )
        this.isProcessing = false
      } catch (error) {
        console.log(error)
        this.isProcessing = false
        this.message = "error occured : " + error.message
      }
      this.$auth_signout()
    },
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
