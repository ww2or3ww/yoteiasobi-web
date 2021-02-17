import { Auth } from 'aws-amplify'

const NEED_AUTHENTICATED_PAGES = ['/user', '/profile']

export default async ({ route, redirect, store }) => {
  if (store.state.authdata.user == null) {
    let isSignedIn = false
    await Auth.currentUserInfo()
      .then(data => {
        isSignedIn = Boolean(data)
        store.commit('authdata/setUser', data)
      })
      .then(() => {
        if (!isSignedIn) {
          if (NEED_AUTHENTICATED_PAGES.indexOf(route.path) >= 0) {
            redirect('/login')
          }
        }
      })
  }
}