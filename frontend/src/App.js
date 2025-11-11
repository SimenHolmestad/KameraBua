import React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import UserPages from './components/UserPages'
import LastImagePage from './components/LastImagePage'
import QrCodePage from './components/QrCodePage'
import QrCodeLastImagePage from './components/QrCodeLastImagePage'
import SlideshowLastImagePage from './components/SlideshowLastImagePage'
import SlideshowPage from './components/SlideshowPage'

import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';


const App = () => {
  const theme = React.useMemo(() => createTheme(), []);
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path='/album/:albumName/last_image' element={<LastImagePage />} />
          <Route path='/album/:albumName/last_image_qr' element={<QrCodeLastImagePage />} />
          <Route path='/album/:albumName/slideshow' element={<SlideshowPage />} />
          <Route path='/album/:albumName/slideshow_last_image' element={<SlideshowLastImagePage />} />
          <Route path='/qr' element={<QrCodePage />} />
          <Route path='/*' element={<UserPages />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;
