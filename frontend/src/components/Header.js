import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import CameraIcon from '@mui/icons-material/PhotoCamera';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button'
import { Link } from 'react-router-dom';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  logo: {
    textDecoration: "inherit",
    color: "inherit",
    textTransform: "none"
  }
}));

const Header = () => {
  const classes = useStyles();
  return (
    <AppBar position="relative">
      <Toolbar>
        <Button component={Link} to={ "/" } className={classes.logo} color="inherit">
          <CameraIcon className={classes.icon} />
          <Typography variant="h6" color="inherit" noWrap>
            CameraHub
          </Typography>
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header
