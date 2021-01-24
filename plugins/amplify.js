import Vue from 'vue'
import Amplify from 'aws-amplify'
//import awsconfig from '@/src/aws-exports'
const awsconfig = {
    "aws_project_region": "ap-northeast-1",
    "aws_cognito_identity_pool_id": "",
    "aws_cognito_region": "ap-northeast-1",
    "aws_user_pools_id": "",
    "aws_user_pools_web_client_id": "",
    "oauth": {
        "domain": "",
        "scope": [
            "phone",
            "email",
            "openid",
            "profile",
            "aws.cognito.signin.user.admin"
        ],
        "redirectSignIn": "",
        "redirectSignOut": "",
        "responseType": "code"
    },
    "federationTarget": "COGNITO_USER_POOLS"
};

awsconfig.aws_cognito_identity_pool_id = process.env.ENV_VAL_aws_cognito_identity_pool_id;
awsconfig.aws_user_pools_id = process.env.ENV_VAL_aws_user_pools_id;
awsconfig.aws_user_pools_web_client_id = process.env.ENV_VAL_aws_user_pools_web_client_id;
awsconfig.oauth.domain = process.env.ENV_VAL_oauth_domain;
awsconfig.oauth.redirectSignIn = process.env.ENV_VAL_oauth_redirectSignIn;
awsconfig.oauth.redirectSignOut = process.env.ENV_VAL_oauth_redirectSignOut;
Amplify.configure(awsconfig)

Vue.use(Amplify)
