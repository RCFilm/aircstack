import React from 'react';
import { ThemeProvider, useTheme } from './theme.jsx';
import { useAuth } from './auth';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './components/ui/Tabs';
import LoginForm from './components/ui/LoginForm';
import ContainersPanel from './components/ContainersPanel';
import VolumesPanel from './components/VolumesPanel';
import SecretsPanel from './components/SecretsPanel';
import ConfigsPanel from './components/ConfigsPanel';
import AuditLogPanel from './components/AuditLogPanel';

function MainApp() {
  const { dark, setDark } = useTheme();
  const { user, logout } = useAuth();

  if (!user) return <LoginForm />;
  return (
    <div className={dark ? 'dark' : ''}>
      <header>
        <h1>AiRCStack</h1>
        <button onClick={() => setDark(!dark)}>
          {dark ? '🌙' : '☀️'}
        </button>
        <button onClick={logout}>Logout</button>
      </header>
      <Tabs defaultValue="containers">
        <TabsList>
          <TabsTrigger value="containers">Containers</TabsTrigger>
          <TabsTrigger value="volumes">Volumes</TabsTrigger>
          <TabsTrigger value="secrets">Secrets</TabsTrigger>
          <TabsTrigger value="configs">Configs</TabsTrigger>
          <TabsTrigger value="audit">Audit Log</TabsTrigger>
        </TabsList>
        <TabsContent value="containers"><ContainersPanel /></TabsContent>
        <TabsContent value="volumes"><VolumesPanel /></TabsContent>
        <TabsContent value="secrets"><SecretsPanel /></TabsContent>
        <TabsContent value="configs"><ConfigsPanel /></TabsContent>
        <TabsContent value="audit"><AuditLogPanel /></TabsContent>
      </Tabs>
    </div>
  );
}

export default function App() {
  return (
    <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
      <ThemeProvider>
        <MainApp />
      </ThemeProvider>
    </GoogleOAuthProvider>
  );
}
