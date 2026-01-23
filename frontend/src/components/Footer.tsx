import React from 'react';
import Typography from '@mui/material/Typography';
import { makeStyles } from '@mui/styles';
import type { Theme } from '@mui/material/styles';

const useStyles = makeStyles((theme: Theme) => ({
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

const Footer = () => {
  const classes = useStyles();
  return (
    <footer className={classes.footer}>
      <Typography variant="h6" align="center" gutterBottom color="inherit">
        Hope you like CameraHub!
      </Typography>
      <Typography variant="subtitle1" align="center" color="inherit" component="p">
        CameraHub is made using Python, FastAPI, React and Material UI. The source code is openly available on{' '}
        <a
          className={classes.footerLink}
          href="https://github.com/SimenHolmestad/CameraHub"
          target="_blank"
          rel="noreferrer"
        >
          GitHub
        </a>
        .
      </Typography>
    </footer>
  );
};

export default Footer;
