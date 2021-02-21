<template>
  <v-avatar
    size="160"
    :style="avatarStyle"
    @click="selectedAvatar"
    @dragenter="dragEnterAvatar"
    @dragleave="dragLeaveAvatar"
    @dragover.prevent="dragOverAvatar"
    @drop.prevent="dropFileAvatar"
  >
    <input
      style="display: none"
      ref="input"
      type="file"
      accept="image/jpeg, image/jpg, image/png"
      @change="selectedInput"
    >
    <v-img :src="propsImageSrc" />
  </v-avatar>
</template>

<script>
export default {
  props: {
    propsImageSrc: {
      type: String, 
      required: true
    },
    callbackSelectedPicture: {
      type: Function, 
      required: true
    },
  },
  data() {
    return {
      selectedImage: null,
      avatarStyle:{
        border: '2px solid #000'
      },
    }
  },
  methods: {
    selectedAvatar() {
      this.$refs.input.click()
    },
    dragEnterAvatar() {
      this.avatarStyle.border = '4px solid #448AFF'
    },
    dragOverAvatar() {
      this.avatarStyle.border = '4px solid #448AFF'
    },
    dragLeaveAvatar() {
      this.avatarStyle.border = '2px solid #000'
    },
    dropFileAvatar() {
      this.avatarStyle.border = '2px solid #000'
      const file = [...event.dataTransfer.files][0]
      this.setImageToAvatar(file)
    },
    selectedInput() {
      const file = this.$refs.input.files[0]
      this.setImageToAvatar(file)
    },
    setImageToAvatar(file) {
      if (file) {
        this.callbackSelectedPicture(file)
      }
    }
  },
}
</script>
