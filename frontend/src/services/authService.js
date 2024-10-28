import axios from 'axios';

export const login = (uid, password) => {
  return axios.post('/api/logincheck', { uid, password });
};

export const checkSession = () => {
  return axios.get('/api/session-check');
};

export const logout = () => {
  return axios.get('/api/logout');
};