import React from 'react';
import Menu from './Menu';
import AlbumPage from './AlbumPage';
import Typography from '@mui/material/Typography';
import { makeStyles } from '@mui/styles';
import Header from './Header';
import { Route, Routes } from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  footer: {
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    padding: theme.spacing(6),
  },
  footerLink: {
    color: theme.palette.primary.contrastText,
    textDecoration: 'none',
    fontWeight: 600,
  },
}));

const UserPages = () => {
  const classes = useStyles();
  return (
    <>
      <Header/>
      {/* content */}
      <Routes>
        <Route path='album/:albumName/*' element={<AlbumPage />} />
        <Route index element={<Menu />} />
      </Routes>
      {/* Footer */}
      <footer className={classes.footer}>
        <Typography variant="h6" align="center" gutterBottom color="inherit">
          Hope you like CameraHub!
        </Typography>
        <Typography variant="subtitle1" align="center" color="inherit" component="p">
          CameraHub is made using Python, Flask, React and Material UI. The source code is openly available on <a className={classes.footerLink} href="https://github.com/SimenHolmestad/CameraHub" target="_blank" rel="noreferrer">GitHub</a>.
        </Typography>
      </footer>
    </>
  );
};

export default UserPages
