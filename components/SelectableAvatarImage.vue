<template>
  <v-avatar
    :tile="isTile"
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
      id="inputfile"
    >
    <v-img :src="imageAddressTmp" />
  </v-avatar>
</template>

<script>
export default {
  props: {
    propsImageSrc: {
      type: String
    },
    callbackSelectedPicture: {
      type: Function, 
      required: false
    },
    isTile: {
      type: Boolean,
      default: false
    },
  },
  watch: {
    propsImageSrc (nextValue) {
      this.imageAddressTmp = nextValue
      const obj = document.getElementById("inputfile")
      obj.value = ""
    },
  },
  data() {
    return {
      selectedImage: null,
      imageAddressTmp: "",
      avatarStyle:{
        border: '2px solid #000'
      },
    }
  },
  methods: {
    selectedAvatar() {
      if (this.callbackSelectedPicture) {
        this.$refs.input.click()
      }
    },
    dragEnterAvatar() {
      if (this.callbackSelectedPicture) {
        this.avatarStyle.border = '4px solid #448AFF'
      }
    },
    dragOverAvatar() {
      if (this.callbackSelectedPicture) {
        this.avatarStyle.border = '4px solid #448AFF'
      }
    },
    dragLeaveAvatar() {
      if (this.callbackSelectedPicture) {
        this.avatarStyle.border = '2px solid #000'
      }
    },
    dropFileAvatar() {
      if (this.callbackSelectedPicture) {
        this.avatarStyle.border = '2px solid #000'
        const file = [...event.dataTransfer.files][0]
        this.setImageToAvatar(file)
      }
    },
    selectedInput() {
      if (this.callbackSelectedPicture) {
        const file = this.$refs.input.files[0]
        this.setImageToAvatar(file)
      }
    },
    setImageToAvatar(file) {
      if (file) {
        this.callbackSelectedPicture(file)
      }
    }
  },
}
</script>
