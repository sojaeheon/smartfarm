import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    isLoggedIn: false,
    userId: null,
    device_name: null,
  },
  mutations: {
    SET_LOGIN(state, payload) {
      state.isLoggedIn = true;
      state.userId = payload.userId;
      state.device_name = payload.device_name;
    },
    LOGOUT(state) {
      state.isLoggedIn = false;
      state.userId = null;
      state.device_name= null;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        console.log(credentials);
        const response = await axios.post('/api/logincheck', credentials, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (response.data.success) {
          commit('SET_LOGIN', {
            userId: response.data.session.username,
            device_name: response.data.session.device_name,
          });
        } else {
          throw new Error('Invalid login credentials');
        }
      } catch (error) {
        console.error("An error occurred:", error);
      }
    },
    async logout({ commit }) {
      await axios.get('/api/logout');
      commit('LOGOUT');
    },
    async checkSession({ commit }) {
      try {
        const response = await axios.get('/api/session-check');
        if (response.data.loggedIn) {
          commit('SET_LOGIN', {
            userId: response.data.username,
            device_name:response.data.device_name
          });
        }
      } catch (error) {
        console.error("Session check failed:", error.response ? error.response.data : error.message);
      }
    },
  },
});

export default store;
