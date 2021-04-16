export const state = () => ({
  user_obj: null,
  user: null,
  picture: null
})

export const getters = {
  picture(state) {
    return state.picture
  },
  user(state) {
    return state.user
  }
}

export const mutations = {
  setUser(state, user) {
    state.user_obj = user
    state.user = JSON.parse(JSON.stringify(user))
  },
  setPicture(state, picture) {
    state.picture = picture
  },
  clearUser(user) {
    state.user_objuser = null
    state.user = null
    state.picture = null
  }
}