export default (context, inject) => {
  const COOKIE_KEY_CERTIFIED_FLG = 'yoteiasobi.w2or3w.com/certified-flg'
  
  const setCertifiedFlgFunc = (flg) => {
    context.app.$cookies.set(COOKIE_KEY_CERTIFIED_FLG, flg, {
      path: '/',
      maxAge: 60 * 60 * 24 * 3
    })
  }
  
  const getCertifiedFlgFunc = () => {
    return context.app.$cookies.get(COOKIE_KEY_CERTIFIED_FLG)
  }
  
  inject('cookie_set_certified_flg', setCertifiedFlgFunc)
  inject('cookie_get_certified_flg', getCertifiedFlgFunc)
}