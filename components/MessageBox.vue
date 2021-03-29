<template>
  <div class="text-center">
    <v-card>
      <v-card-title>
        {{ titleTmp }}
      </v-card-title>

      <v-card-text style="text-align: left; padding-bottom: 0;">
        {{ text1 }}
      </v-card-text>
      <v-card-text style="text-align: left; padding-top: 0; padding-bottom: 0;">
        {{ text2 }}
      </v-card-text>
      <v-card-text style="text-align: left; padding-top: 0;">
        {{ text3 }}
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          text
          @click="onClickOK"
        >
          OK
        </v-btn>
        <v-btn
          v-if="isShowCancel"
          color="primary"
          text
          @click="onClickCancel"
        >
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String
    },
    text: {
      type: String, 
      required: true
    },
    callbackBtn: {
      type: Function, 
      required: true
    },
    isShowCancel: {
      type: Boolean,
      default: true
    },
  },
  watch: {
    text (nextValue) {
      this.convertTexts(nextValue)
    },
  },
  data() {
    return {
      titleTmp: "",
      text1: "",
      text2: "",
      text3: "",
    }
  },
  mounted () {
    this.convertTexts(this.text)
    this.titleTmp = this.title
    if (!this.titleTmp) {
      this.titleTmp = "YOTEIASOBI"
    }
  },
  methods: {
    convertTexts(value) {
      this.text1 = ""
      this.text2 = ""
      this.text3 = ""
      const words = value.split('\n');
      if (words.length > 0) {
        this.text1 = words[0]
      }
      if (words.length > 1) {
        this.text2 = words[1]
      }
      if (words.length > 2) {
        this.text3 = words[2]
      }
    },
    onClickOK() {
      this.callbackBtn("ok")
    },
    onClickCancel() {
      this.callbackBtn("cancel")
    },
  },
}
</script>
