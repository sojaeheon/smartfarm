// store.js (Vue 3용)
import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    isLoggedIn: false,
    userId: null,
    rapaIp: null,
    port: null,
  },
  mutations: {
    SET_LOGIN(state, payload) {
      state.isLoggedIn = true;
      state.userId = payload.userId;
      state.rapaIp = payload.rapaIp;
      state.port = payload.port;
    },
    LOGOUT(state) {
      state.isLoggedIn = false;
      state.userId = null;
      state.rapaIp = null;
      state.port = null;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      console.log(credentials);
      const response = await axios.post('/api/logincheck', credentials);
      if (response.data.success) {
        commit('SET_LOGIN', {
          userId: response.data.uid,
          rapaIp: response.data.rapa_ip,
          port: response.data.port,
        });
      } else {
        throw new Error('Invalid login credentials');
      }
    },
    async logout({ commit }) {
      await axios.post('/api/logout');
      commit('LOGOUT');
    },
    async checkSession({ commit }) {
      const response = await axios.get('/api/session-check');
      if (response.data.loggedIn) {
        commit('SET_LOGIN', {
          userId: response.data.uid,
          rapaIp: response.data.rapa_ip,
          port: response.data.port,
        });
      }
    },
  },
});

export default store;
