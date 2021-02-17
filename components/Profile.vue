<template>
  <div class="main">
    <section class="section_avatar">
      <SelectableAvatarImage :image_src="picture" />
    </section>
    
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
        color="#424242"
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
        <v-icon right dark>mdi-cloud-upload</v-icon>
      </v-btn>
    </section>
    
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
export default {
  components: {
    SelectableAvatarImage,
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
      isFormValid: false,
      isProcessing: false,
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
      
      this.name_org = this.name
      this.email_org = this.email
      this.comment_org = this.comment
      
      this.isProcessing = false
    },
    isEdited(){
      return this.name != this.name_org || this.comment != this.comment_org
    },
    onUpdate() {
      this.updateProcess()
    },
    onUpdateCompleted() {
      this.$auth_reload_user(this.dataInitialize)
    },
    onCancel() {
      this.name = this.name_org
      this.comment = this.comment_org
    },
    async updateProcess() {
      this.isProcessing = true
      try {
        const postdata = {
          headers: {},
          body: {
            'name': this.name,
            'comment': this.comment
          },
          response: true,
        };
        const response = await API.post(
          process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
          '/profile', 
          postdata
        ).then(response => {
          setTimeout(this.onUpdateCompleted, 3000)
        })
      } catch (error) {
        console.log(error)
        this.isProcessing = false
        this.message = error.message + 'が発生しました。'
      }
    }
  },
}
</script>
<style>
.main {
  background-color: #757575;
  padding: 8px;
}
.section_avatar {
  text-align: center;
  margin: 24px;
}
.outlined {
    border: 4px solid #00F;
}
.section_buttons {
  text-align: right;
  margin: 40px 16px 16px 16px;
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
