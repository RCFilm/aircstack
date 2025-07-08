import React, { useState } from 'react';
import { useAuth } from '../../auth';
import { GoogleLogin } from '@react-oauth/google';
export default function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, loginWithGoogle } = useAuth();
  return (
    <>
      <form onSubmit={e => { e.preventDefault(); login(username, password); }}>
        <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </form>
      <div style={{ marginTop: '1rem' }}>
        <GoogleLogin onSuccess={loginWithGoogle} onError={() => {}} />
      </div>
    </>
  );
}
