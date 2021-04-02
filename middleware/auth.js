import { Auth, Storage } from 'aws-amplify'

const NEED_AUTHENTICATED_PAGES  = ['/profile', '/users']
const NEED_ADMIN_PAGES          = ['/users']

export default async (context) => {
  console.log(">>>>")
  console.log(context.route.path)
  if (context.store.state.authdata.user == null) {
    let user = await Auth.currentUserInfo()
    try {
      if (user) {
        const image = await context.$auth_get_picture_address_from_storage(user)
        context.store.commit('authdata/setUser', user)
        context.store.commit('authdata/setPicture', image)
      }
    } catch (e) {
      user = null
    }
    if (user == null) {
      if (NEED_AUTHENTICATED_PAGES.indexOf(context.route.path) == 0) {
        context.redirect('/login')
      }
    }
  } else {
    if (NEED_ADMIN_PAGES.indexOf(context.route.path) == 0) {
      const isAdmin = context.$auth_is_admin()
      if (isAdmin != "1") {
        context.redirect('/')
      }
    }
  }
}
