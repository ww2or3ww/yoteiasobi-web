import colors from 'vuetify/es5/util/colors'

export default {
  mode: 'spa',

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    htmlAttrs: {
      prefix: 'og: http://ogp.me/ns#'
    },
    titleTemplate: '%s',
    title: 'YOTEIASOBI',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'og:type', property: 'og:type', content: 'website' },
      { hid: 'twitter:card', name: 'twitter:card', content: 'summary_large_image' },
      { hid: 'twitter:site', name: 'twitter:site', content: '@w2or3w' },
      {
        hid: 'description',
        name: 'description',
        content: 'よてい で あそぼ！YOTEIASOBI は Googleカレンダーを ゆるっと共有 できる サーバーレスWebアプリです。'
      },
      {
        hid: 'og:site_name',
        property: 'og:site_name',
        content: 'YOTEIASOBI'
      },
      {
        hid: 'og:url',
        property: 'og:url',
        content: 'https://yoteiasobi.w2or3w.com'
      },
      {
        hid: 'og:title',
        property: 'og:title',
        content: 'YOTEIASOBI'
      },
      {
        hid: 'og:description',
        property: 'og:description',
        content: 'よてい で あそぼ！'
      },
      {
        hid: 'og:image',
        property: 'og:image',
        content: 'https://near-near-map.s3-ap-northeast-1.amazonaws.com/images/resources/yoteiasobi-ogp.png'
      },
    ],
    link: [
      { 
        rel: 'icon', 
        type: 'image/x-icon', 
        href: '/img/favicon.png'
      },
      { rel: 'apple-touch-icon', type: 'image/x-icon',sizes:"57x57",    href: `/img/apple-touch-icon-57x57.png` },
      { rel: 'apple-touch-icon', type: 'image/x-icon',sizes:"72x72",    href: `/img/apple-touch-icon-72x72.png` },
      { rel: 'apple-touch-icon', type: 'image/x-icon',sizes:"76x76",    href: `/img/apple-touch-icon-76x76.png` },
      { rel: 'apple-touch-icon', type: 'image/x-icon',sizes:"114x114",  href: `/img/apple-touch-icon-114x114.png` },
      { rel: 'apple-touch-icon', type: 'image/x-icon',sizes:"120x120",  href: `/img/apple-touch-icon-120x120.png` },
      { rel: 'apple-touch-icon', type: 'image/x-icon',sizes:"144x144",  href: `/img/apple-touch-icon-144x144.png` },
      { rel: 'apple-touch-icon', type: 'image/x-icon',sizes:"152x152",  href: `/img/apple-touch-icon-152x152.png` },
      { rel: 'apple-touch-icon', type: 'image/x-icon',sizes:"180x180",  href: `/img/apple-touch-icon-180x180.png` },
      {
        rel: 'stylesheet', 
        href: 'https://fonts.googleapis.com/css2?family=Train%20One'
      }
    ],
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
    ENVVAL_GCP_CALENDAR_ID_SAMPLE: process.env.ENVVAL_GCP_CALENDAR_ID_SAMPLE,
    ENVVAL_GCP_SERVICE_ACCOUNT: process.env.ENVVAL_GCP_SERVICE_ACCOUNT,
    ENVVAL_GOOGLE_ANALYTICS_ID: process.env.ENVVAL_GOOGLE_ANALYTICS_ID
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
    [
      '@nuxtjs/google-analytics',
      {
        id: process.env.ENVVAL_GOOGLE_ANALYTICS_ID
      }
    ],
  ],
  manifest: {
    name: 'YOTEIASOBI',
    lang: 'ja',
    description: 'よてい で あそぼ！',
    theme_color: '#FF8080',
    background_color: '#272727',
    display: 'standalone',
    Scope: '/',
    start_url: '/',
    splash_pages: null
  },
  
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
  
  // Moment
  moment: {
    locales: ['ja']
  },
}
