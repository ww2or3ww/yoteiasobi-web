import { Auth } from 'aws-amplify'

export default (context, inject) => {
  
  const signinFunc = (providerName) => {
    context.app.$cookie_set_certified_flg(true)
    Auth.federatedSignIn({ provider: providerName })
  }
  
  const signoutFunc = () => {
    context.store.commit('authdata/clearUser')
    context.app.$cookie_set_certified_flg(false)
    Auth.signOut()
  }
  
  const reloadUserFunc = (callback) => {
    Auth.currentUserInfo()
      .then(data => {
        context.store.commit('authdata/setUser', data)
        if (callback) {
          callback()
        }
      })
  }
  
  const isAuthedFunc = () => {
    return context.store.state.authdata.user != null
  }
  
  const getNameFunc = () => {
    const user = JSON.parse(JSON.stringify(context.store.state.authdata.user))
    if (user == null) {
      return "Guest"
    }
    return user.attributes["custom:name"]
  }

  const getEMailFunc = () => {
    const user = JSON.parse(JSON.stringify(context.store.state.authdata.user))
    if (user == null) {
      return ""
    }
    return user.attributes["custom:email"]
  }
  
  const getPictureFunc = () => {
    const user = JSON.parse(JSON.stringify(context.store.state.authdata.user))
    if (user == null) {
      return null
    }
    return user.attributes["custom:picture"]
  }

  const getCommentFunc = () => {
    const user = JSON.parse(JSON.stringify(context.store.state.authdata.user))
    if (user == null) {
      return null
    }
    return user.attributes["custom:comment"]
  }

  inject('auth_signin', signinFunc)
  inject('auth_signout', signoutFunc)
  inject('auth_reload_user', reloadUserFunc)
  inject('auth_is_authed', isAuthedFunc)
  inject('auth_get_name', getNameFunc)
  inject('auth_get_email', getEMailFunc)
  inject('auth_get_picture', getPictureFunc)
  inject('auth_get_comment', getCommentFunc)
}