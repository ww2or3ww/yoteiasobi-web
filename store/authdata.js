export const state = () => ({
  user: null,
  picture: null
})

export const getters = {
  picture(state) {
    return state.picture
  }
}

export const mutations = {
  setUser(state, user) {
    state.user = user
  },
  setPicture(state, picture) {
    state.picture = picture
  },
  clearUser(user) {
    state.user = null
    state.picture = null
  }
}