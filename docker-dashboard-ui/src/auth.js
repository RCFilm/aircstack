import { useState } from 'react';
import { api } from './api';

export function useAuth() {
  const [user, setUser] = useState(() => localStorage.getItem('user'));
  async function login(username, password) {
    const res = await api.post('/auth/login', { username, password });
    localStorage.setItem('jwt', res.data.token);
    localStorage.setItem('user', username);
    setUser(username);
  }
  async function loginWithGoogle(credentialResponse) {
    const res = await api.post('/auth/google', { token: credentialResponse.credential });
    localStorage.setItem('jwt', res.data.token);
    localStorage.setItem('user', res.data.user);
    setUser(res.data.user);
  }
  function logout() {
    localStorage.removeItem('jwt');
    localStorage.removeItem('user');
    setUser(null);
  }
  return { user, login, loginWithGoogle, logout };
}
