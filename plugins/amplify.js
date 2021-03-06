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
    "federationTarget": "COGNITO_USER_POOLS",
    "aws_cloud_logic_custom": [
        {
            "name": "",
            "endpoint": "",
            "region": "ap-northeast-1"
        }
    ],
    "aws_appsync_graphqlEndpoint": "",
    "aws_appsync_region": "ap-northeast-1",
    "aws_appsync_authenticationType": "AMAZON_COGNITO_USER_POOLS",
    "aws_user_files_s3_bucket": "",
    "aws_user_files_s3_bucket_region": "ap-northeast-1"
};
awsconfig.aws_cognito_identity_pool_id          = process.env.ENVVAL_AWS_EXPORTS_aws_cognito_identity_pool_id;
awsconfig.aws_user_pools_id                     = process.env.ENVVAL_AWS_EXPORTS_aws_user_pools_id;
awsconfig.aws_user_pools_web_client_id          = process.env.ENVVAL_AWS_EXPORTS_aws_user_pools_web_client_id;
awsconfig.oauth.domain                          = process.env.ENVVAL_AWS_EXPORTS_oauth_domain;
awsconfig.oauth.redirectSignIn                  = process.env.ENVVAL_AWS_EXPORTS_oauth_redirectSignIn;
awsconfig.oauth.redirectSignOut                 = process.env.ENVVAL_AWS_EXPORTS_oauth_redirectSignOut;
awsconfig.aws_cloud_logic_custom[0].name        = process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name;
awsconfig.aws_cloud_logic_custom[0].endpoint    = process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_endpoint;
awsconfig.aws_user_files_s3_bucket              = process.env.ENVVAL_AWS_EXPORTS_aws_user_files_s3_bucket;
awsconfig.aws_appsync_graphqlEndpoint           = process.env.ENVVAL_AWS_EXPORTS_aws_appsync_graphqlEndpoint;

Amplify.configure(awsconfig)
Vue.use(Amplify)
