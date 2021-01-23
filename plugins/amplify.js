import Vue from 'vue'
import Amplify from 'aws-amplify'
import awsconfig from '@/src/aws-exports'

awsconfig.oauth.redirectSignIn = `${window.location.origin}/`;
awsconfig.oauth.redirectSignOut = `${window.location.origin}/`;
    
Amplify.configure(awsconfig)
Vue.use(Amplify)
