<template>
  <v-btn
    :color="color"
    :disabled=isDisabled
    @click="onClick"
  >
    <v-container>
      <v-row>
        <v-col cols="2">
          <v-icon left dark v-if="!isRight">{{icon}}</v-icon>
        </v-col>
        <v-col cols="8">
          {{text}}
        </v-col>
        <v-col cols="2">
          <v-icon left dark v-if="isRight">{{icon}}</v-icon>
        </v-col>
      </v-row>
    </v-container>
  </v-btn>
</template>

<script>
export default {
  props: {
    mytype: {
      type: String, 
      required: true
    },
    text: {
      type: String, 
      required: true
    },
    color: {
      type: String, 
      required: true
    },
    icon: {
      type: String, 
      required: true
    },
    isDisabled: {
      type: Boolean, 
      default: false
    },
    isRight: {
      type: Boolean, 
      default: false
    },
    callbackClick: {
      type: Function, 
      required: true
    },
  },
  methods: {
    onClick() {
      this.callbackClick(this.mytype)
    },
  },
}
</script>
