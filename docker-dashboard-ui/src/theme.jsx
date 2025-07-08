import { createContext, useState, useEffect, useContext } from 'react';
const ThemeContext = createContext();
export function ThemeProvider({ children }) {
  const [dark, setDark] = useState(() =>
    window.matchMedia('(prefers-color-scheme: dark)').matches
  );
  useEffect(() => {
    document.body.className = dark ? 'dark' : '';
  }, [dark]);
  return (
    <ThemeContext.Provider value={{ dark, setDark }}>
      {children}
    </ThemeContext.Provider>
  );
}
export function useTheme() {
  return useContext(ThemeContext);
}
