import { Auth, Storage } from 'aws-amplify'

const NEED_AUTHENTICATED_PAGES  = ['/profile', '/users']
const NEED_ADMIN_PAGES          = ['/users']

export default async (context) => {
  
  const isInclude = (list, path) => {
    const data = list.filter(tmp => {
      return path.indexOf(tmp) == 0
    })
    return data.length > 0
  }
  
  const isFree = (path) => {
    return (path == '/' || path == '/login')
  }
  
  let user = null
  if (context.store.state.authdata.user == null) {
    user = await Auth.currentUserInfo()
    try {
      if (user) {
        const image = await context.$auth_get_picture_address_from_storage(user)
        context.store.commit('authdata/setUser', user)
        context.store.commit('authdata/setPicture', image)
      }
    } catch (e) {
      user = null
    }
  } else {
    user = context.store.state.authdata.user
  }
  
  if (isFree(context.route.path)) {
    return
  }
  
  if (user == null) {
    if(isInclude(NEED_AUTHENTICATED_PAGES, context.route.path)) {
      context.redirect('/login')
    }
  } else {
    if(isInclude(NEED_ADMIN_PAGES, context.route.path)) {
      const isAdmin = context.$auth_is_admin()
      if (!isAdmin) {
        context.redirect('/')
      }
    }
  }
}
