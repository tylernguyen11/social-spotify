// import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { BrowserRouter as Router, Route, Routes } from 'react-router';
import SpotifyCallback from './components/SpotifyCallback/SpotifyCallback.tsx';
import Profile from './components/Profile/Profile.tsx'
import ArtistPage from './components/Artist/ArtistPage.tsx';
import Header from './components/Header/Header.tsx';
import '@mantine/core/styles.css';
import { createTheme, MantineProvider } from '@mantine/core';

const theme = createTheme({
  fontFamily: 'sans-serif',
  primaryColor: 'green',
});

const username = localStorage.getItem('username');

createRoot(document.getElementById('root')!).render(
  <MantineProvider theme={theme}>
    <div>
      <Router>
        <Header username={username} />
        <Routes>
          <Route path='/' element={<App />} />
          <Route path='/callback' element={<SpotifyCallback />} />
          <Route path='/profile/:username' element={<Profile />} />
          <Route path="/artists/:id" element={<ArtistPage />} />
        </Routes>
      </Router>
    </div>
  </MantineProvider>
)
