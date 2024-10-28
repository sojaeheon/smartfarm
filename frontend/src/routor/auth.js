import axios from 'axios';

const state = {
  loggedIn: false,
  userInfo: {},
};

const mutations = {
  SET_LOGIN_STATE(state, loggedIn) {
    state.loggedIn = loggedIn;
  },
  SET_USER_INFO(state, userInfo) {
    state.userInfo = userInfo;
  },
  LOGOUT(state) {
    state.loggedIn = false;
    state.userInfo = {};
  },
};

const actions = {
  async login({ commit }, loginData) {
    try {
      const response = await axios.post('/api/logincheck', loginData);
      if (response.data.success) {
        commit('SET_LOGIN_STATE', true);
        commit('SET_USER_INFO', response.data.session);
      } else {
        commit('SET_LOGIN_STATE', false);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  },
  async checkSession({ commit }) {
    try {
      const response = await axios.get('/api/session-check');
      if (response.data.loggedIn) {
        commit('SET_LOGIN_STATE', true);
        commit('SET_USER_INFO', response.data.session);
      } else {
        commit('SET_LOGIN_STATE', false);
      }
    } catch (error) {
      console.error('Session check error:', error);
    }
  },
  async logout({ commit }) {
    try {
      await axios.get('/api/logout');
      commit('LOGOUT');
    } catch (error) {
      console.error('Logout error:', error);
    }
  },
};

export default {
  state,
  mutations,
  actions,
};
