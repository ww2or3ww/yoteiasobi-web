<template>
  <v-row justify="center">
    <v-col>
      <v-flex xs12 sm12 md12>
        <v-card>
          <v-card-title class="common-card-title">
            <p class="common-p-card-title" style="margin: 0;">About</p>
          </v-card-title>
        </v-card>
        
        <v-card style="margin-top: 4px;">
          <v-card-text class="card-text">
            <p class="font-card-text" style="margin: 0;">
              当Webサービスは、以下の目的・動機のために開発・運用しています。
            </p>
            <ul>
              <li class="font-card-text">
                自身のスキルアップのため。
              </li>
            </ul>
          </v-card-text>
    
          <v-card-title class="common-card-title">
            <p class="common-p-card-subtitle" style="margin: 0;">
              プライバシーポリシー
            </p>
          </v-card-title>
          <v-card-text class="card-text">
            <p class="font-card-text" style="margin: 0;">
              以下の点をご承知いただいた上でご利用ください。
            </p>
            <ul>
              <li class="font-card-text">
                サービスをご利用された結果発生した損害について、開発者は一切の責任を負いかねます。
              </li>
            </ul>
            <p class="font-card-text" style="margin: 0;">
              プライバシーポリシーや利用規約の詳細については ->
              <router-link to="/about_policy">
                こちら
              </router-link>
            </p>
          </v-card-text>
    
          <v-card-title class="common-card-title">
            <p class="common-p-card-subtitle" style="margin: 0;">テクニカル</p>
          </v-card-title>
          <v-card-text class="card-text">
            <p class="font-card-text" style="margin: 0;">
              以下の技術を利用しています。
            </p>
            <ul>
              <li class="font-card-text">
                Nuxt.js, Vuetify
              </li>
              <li class="font-card-text">
                AWS Amplify, Cognito, API Gateway, Lambda(Python), AppSync, DynamoDB, S3
              </li>
              <li class="font-card-text">
                Google Calendar API, Google OAuth
              </li>
            </ul>
            <p></p>
            
            <p class="font-card-text" style="margin: 0;">
              アーキテクチャは以下のような感じ。
            </p>
            <v-img
              src="https://near-near-map.s3-ap-northeast-1.amazonaws.com/resource/image/yoteiasobi-architecture.png"
              width="50%"
              max-width="160px"
              @click.stop="showArchitecture = true"
            ></v-img>
            <v-dialog v-model="showArchitecture" max-width="85vw">
              <img
                src="https://near-near-map.s3-ap-northeast-1.amazonaws.com/resource/image/yoteiasobi-architecture.png"
                width="100%"
                @click.stop="showArchitecture = false"
              />
            </v-dialog>
          </v-card-text>
  
          <v-card-text class="card-text">
            <p class="font-card-text" style="margin: 0;">
              お気付きの点やご意見・ご要望などございましたら、お気軽にSNS等へメッセージください。
            </p>
          </v-card-text>
        </v-card>
        <v-card>
          <v-card-title>
            <v-btn
              class="mx-2"
              fab
              small
              color="white"
              href="https://twitter.com/w2or3w"
              target="_blank"
            >
              <v-icon color="#333333" size="28px">mdi-twitter</v-icon>
            </v-btn>
            <v-btn
              class="mx-2"
              fab
              small
              color="white"
              href="https://www.facebook.com/w2or3w"
              target="_blank"
            >
              <v-icon color="#333333" size="28px">mdi-facebook</v-icon>
            </v-btn>
            <v-btn
              class="mx-2"
              fab
              small
              color="white"
              href="https://www.instagram.com/w2or3w"
              target="_blank"
            >
              <v-icon color="#333333" size="28px">mdi-instagram</v-icon>
            </v-btn>
            <v-btn
              class="mx-2"
              fab
              small
              color="white"
              href="https://github.com/ww2or3ww"
              target="_blank"
            >
              <v-icon color="#333333" size="28px">mdi-github</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <p class="index-foot" style="margin: 0; padding-left: 8px;">
              yoteiasobi.w2or3w.com
            </p>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-col>
  </v-row>
</template>
<script>
export default {
  data() {
    return {
      showArchitecture: false
    }
  }
}
</script>