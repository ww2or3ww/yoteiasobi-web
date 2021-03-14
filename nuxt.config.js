import colors from 'vuetify/es5/util/colors'

export default {
  // Disable server-side rendering (https://go.nuxtjs.dev/ssr-mode)
  ssr: false,

  // Target (https://go.nuxtjs.dev/config-target)
  target: 'static',

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    titleTemplate: '%s - yoteiasobi',
    title: 'yoteiasobi',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    { src: '~/plugins/amplify.js', ssr: false },
    { src: '~/plugins/injected-cookie-common.js', ssr: false },
    { src: '~/plugins/injected-auth-common.js', ssr: false },
  ],
  env: {
    TSC_WATCHFILE: 'UseFsEventsWithFallbackDynamicPolling',
    ENVVAL_AWS_EXPORTS_aws_cognito_identity_pool_id: process.env.ENVVAL_AWS_EXPORTS_aws_cognito_identity_pool_id,
    ENVVAL_AWS_EXPORTS_aws_user_pools_id: process.env.ENVVAL_AWS_EXPORTS_aws_user_pools_id,
    ENVVAL_AWS_EXPORTS_aws_user_pools_web_client_id: process.env.ENVVAL_AWS_EXPORTS_aws_user_pools_web_client_id,
    ENVVAL_AWS_EXPORTS_oauth_domain: process.env.ENVVAL_AWS_EXPORTS_oauth_domain,
    ENVVAL_AWS_EXPORTS_oauth_redirectSignIn: process.env.ENVVAL_AWS_EXPORTS_oauth_redirectSignIn,
    ENVVAL_AWS_EXPORTS_oauth_redirectSignOut: process.env.ENVVAL_AWS_EXPORTS_oauth_redirectSignOut,
    ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name: process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_name,
    ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_endpoint: process.env.ENVVAL_AWS_EXPORTS_aws_cloud_logic_custom_0_endpoint,
    ENVVAL_AWS_EXPORTS_aws_user_files_s3_bucket: process.env.ENVVAL_AWS_EXPORTS_aws_user_files_s3_bucket,
    ENVVAL_AWS_EXPORTS_aws_appsync_graphqlEndpoint: process.env.ENVVAL_AWS_EXPORTS_aws_appsync_graphqlEndpoint,
    ENVVAL_STRIPE_SECRET_KEY: process.env.ENVVAL_STRIPE_SECRET_KEY,
    ENVVAL_STRIPE_PUBLIC_KEY: process.env.ENVVAL_STRIPE_PUBLIC_KEY,
  },

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/stylelint
    '@nuxtjs/stylelint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
    // https://momentjs.com/
    '@nuxtjs/moment',
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    '@nuxtjs/dotenv',
    'cookie-universal-nuxt',
  ],
  
  router: {
    middleware: [
      'auth',
    ],
  },

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {},

  // Vuetify module configuration (https://go.nuxtjs.dev/config-vuetify)
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: { },
  
  // stripe
  stripe: {
    version: 'v3',
    publishableKey: process.env.ENVVAL_STRIPE_PUBLIC_KEY
  },
  
  // Moment
  moment: {
    locales: ['ja']
  },
}
