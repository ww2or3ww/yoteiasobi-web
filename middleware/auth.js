import { Auth, Storage } from 'aws-amplify'

const NEED_AUTHENTICATED_PAGES = ['/user', '/profile']

export default async ({ route, redirect, store }) => {
  if (store.state.authdata.user == null) {
    let user = await Auth.currentUserInfo()
    try {
      if (user) {
        const image = await getPictureAddressFromStorage(user)
        store.commit('authdata/setUser', user)
        store.commit('authdata/setPicture', image)
      }
    } catch (e) {
      user = null
    }
    if (user == null) {
      if (NEED_AUTHENTICATED_PAGES.indexOf(route.path) >= 0) {
        redirect('/login')
      }
    }
  }
}

const getPictureAddressFromStorage = async (user) => {
  let pictureRet = null
  const picturePath = user.attributes["custom:picture"]
  await Storage.get(picturePath.replace('public/', ''), {
    level: 'public', 
    expires: 60 * 60 * 3
  }).then(result => {
    pictureRet = result;
  })
  return pictureRet
}