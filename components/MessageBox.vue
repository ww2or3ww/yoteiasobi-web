<template>
  <div class="text-center">
    <v-card>
      <v-card-title>
        {{ title }}
      </v-card-title>

      <v-card-text>
        {{ text }}
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
  },
  methods: {
    onClickOK() {
      this.callbackBtn("ok")
    },
    onClickCancel() {
      this.callbackBtn("cancel")
    },
  },
}
</script>
