// import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { BrowserRouter as Router, Route, Routes } from 'react-router';
import SpotifyCallback from './components/SpotifyCallback/SpotifyCallback.tsx';
import Profile from './components/Profile/Profile.tsx'

createRoot(document.getElementById('root')!).render(
  <div>
    <Router>
    <Routes>
      <Route path='/' element={<App />} />
      <Route path='/callback' element={<SpotifyCallback />} /> 
      <Route path='/profile/:username' element={<Profile/>}/>
    </Routes>
  </Router>
  </div>
)
