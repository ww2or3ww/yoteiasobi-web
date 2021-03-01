<template>
  <div class="main">
    <section class="section_avatar">
      <SelectableAvatarImage
        :propsImageSrc="picture"
      />
    </section>
    
    <section class="section_form">
      <v-form>
        <v-text-field
          v-model="name"
          label="Name*"
          dense
          readonly
          class="text_field text-gray"
        />
        <v-text-field
          v-model="email"
          label="Email*"
          dense
          readonly
          class="text_field text-gray"
        />
        <v-textarea
          v-model="comment"
          label="Comment"
          dense
          readonly
          class="text_field text-gray"
        />
      </v-form>
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
      email: "",
      comment: "",
      picture: "", 
      isProcessing: false,
      isCheckDisable: false,
      isShowMessage: false,
      message: "",
    }
  },
  mounted () {
    this.dataInitialize()
  },
  methods: {
    async dataInitialize() {
      this.isProcessing = true
      const user = await this.getUsers()
      this.name = user['name']
      this.email = user['email']
      this.comment = user['comment']
      this.picture = user['imageAddress']
      this.isProcessing = false
    },
    async getUsers() {
      try {
        const user = await API.get(
          process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
          '/profile/' + this.$route.query.username
        )
        user['imageAddress'] = await this.$auth_get_picture_address_from_storage(user)

        return user
      } catch (error) {
        console.log(error)
        this.users = null
      }
    },
    onDisable() {
      this.isShowMessage = true
    },
    async processDisable(typestr) {
      this.isShowMessage = false
      if (typestr == "cancel") {
        return
      }
      this.isProcessing = true
      try {
        const postdata = {
          headers: {},
          body: {
            'username': this.name,
            'enable': false
          },
          response: true,
        };
        const response = await API.post(
          process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name, 
          '/profile', 
          postdata
        )
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
