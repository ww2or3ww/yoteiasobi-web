import { Auth, Storage } from 'aws-amplify'

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
  
  const reloadUserFunc = async (callback) => {
    const user = await Auth.currentUserInfo()
    const image = await getPictureAddressFromStorage(user)
    context.store.commit('authdata/setUser', user)
    context.store.commit('authdata/setPicture', image)
    if (callback) {
      callback()
    }
  }
  
  const getPictureAddressFromStorage = async (data) => {
    let pictureRet = null
    let picturePath = null
    if (data.attributes) {
      picturePath = data.attributes["custom:picture"]
    } else if (data.picture) {
      picturePath = data.picture
    } else if (data.image) {
      picturePath = data.image
    } else {
      return null
    }
    await Storage.get(picturePath.replace('public/', ''), {
      level: 'public', 
      expires: 60 * 60 * 3
    }).then(result => {
      pictureRet = result;
    }).catch(err => {
      console.log(err)
    })
    return pictureRet
  }
  
  const isAuthedFunc = () => {
    return context.store.state.authdata.user && 
      context.store.state.authdata.user.attributes
  }
  
  const getUserIDFunc = () => {
    if (context.store.state.authdata.user == null) {
      return null
    }
    return context.store.state.authdata.user.username
  }
  
  const getNameFunc = () => {
    if (!isAuthedFunc()) {
      return "Guest"
    }
    return context.store.state.authdata.user.attributes["custom:name"]
  }

  const getEMailFunc = () => {
    if (!isAuthedFunc()) {
      return null
    }
    return context.store.state.authdata.user.attributes["email"]
  }
  
  const getPictureFunc = () => {
    if (!isAuthedFunc()) {
      return null
    }
    return context.store.state.authdata.picture
  }

  const getPictureKeyFunc = () => {
    if (!isAuthedFunc()) {
      return null
    }
    return context.store.state.authdata.user.attributes["custom:picture"].replace('public/', '')
  }

  const getCommentFunc = () => {
    if (!isAuthedFunc()) {
      return null
    }
    return context.store.state.authdata.user.attributes["custom:comment"]
  }

  const isAdminFunc = () => {
    if (!isAuthedFunc()) {
      return false
    }
    if (context.store.state.authdata.user.attributes["custom:admin"] == "1") {
      return true
    } else {
      return false
    }
  }

  inject('auth_signin', signinFunc)
  inject('auth_signout', signoutFunc)
  inject('auth_reload_user', reloadUserFunc)
  inject('auth_get_picture_address_from_storage', getPictureAddressFromStorage)
  inject('auth_is_authed', isAuthedFunc)
  inject('auth_is_admin', isAdminFunc)
  inject('auth_get_user_id', getUserIDFunc)
  inject('auth_get_name', getNameFunc)
  inject('auth_get_email', getEMailFunc)
  inject('auth_get_picture', getPictureFunc)
  inject('auth_get_picture_key', getPictureKeyFunc)
  inject('auth_get_comment', getCommentFunc)
}