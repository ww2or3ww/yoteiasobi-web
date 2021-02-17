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
    <v-img :src="image_src" />
  </v-avatar>
</template>

<script>
export default {
  props: {
    image_src: {
      type: String, 
      required: true
    }
  },
  data() {
    return {
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
      console.log(file)
    },
    selectedInput() {
      const file = this.$refs.input.files[0]
      console.log(file)
    }
  },
}
</script>
