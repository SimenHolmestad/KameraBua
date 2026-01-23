import React, { useEffect, useState } from 'react';
import Card from '@mui/material/Card';
import { get_available_album_data, isApiError } from './../server'
import NewAlbumDialog from './NewAlbumDialog';
import { Link, Navigate } from 'react-router-dom';
import { makeStyles } from '@mui/styles';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Grid from '@mui/material/Grid';
import Header from './Header';
import Footer from './Footer';
import type { Theme } from '@mui/material/styles';
import type { AvailableAlbumsResponse } from '../api';
import type { Result } from './../server';

const useAlbumData = (): Result<AvailableAlbumsResponse> | null => {
  const [albumData, setAlbumData] = useState<Result<AvailableAlbumsResponse> | null>(null);
  useEffect(() => {
    get_available_album_data().then((data) => setAlbumData(data));
  }, []);
  return albumData;
};

const useStyles = makeStyles((theme: Theme) => ({
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  albumCardContainer: {
    paddingBottom: "20px",
    minHeight: "50vh"
  },
  card: {
    height: '100%',
    width: '100%',
    marginTop: '20px',
    paddingTop: '10px',
    cursor: 'pointer',
    backgroundColor: theme.palette.background.paper,
    borderRadius: theme.shape.borderRadius * 2 || 8,
    border: `1px solid ${theme.palette.divider}`,
    boxShadow: `0 8px 20px rgba(0,0,0,0.08)`,
    backgroundImage: `linear-gradient(145deg, ${theme.palette.grey[50]}, ${theme.palette.grey[100]})`,
    '&:hover': {
      backgroundColor: theme.palette.grey[50],
      boxShadow: `0 12px 28px rgba(0,0,0,0.12)`,
    },
  },
  albumLink: {
    textDecoration: "inherit",
    color: "inherit",
    textTransform: "none"
  },
  albumLinkText: {
    fontWeight: '200',
    color: theme.palette.primary.main,
  },
  loadingGrid: {
    paddingTop: "30px",
    paddingBottom: "10px",
  }
}));

const FrontPage = () => {
  const albumData = useAlbumData();
  const classes = useStyles();
  const [dialogOpen, setDialogOpen] = React.useState(false);

  let albumList = null
  if (!albumData) {
    return (
      <>
        <Header />
        <Grid container className={classes.loadingGrid} spacing={2} justifyContent="center">
          <CircularProgress />
        </Grid>
        <Footer />
      </>
    )
  } else if (isApiError(albumData)) {
    return (
      <>
        <Header />
        <Container maxWidth="sm" className={classes.loadingGrid}>
          <Typography variant="h6" align="center" color="error">
            {albumData.error}
          </Typography>
        </Container>
        <Footer />
      </>
    )
  } else if (albumData.forced_album) {
    return (
      <>
        <Header />
        <Navigate to={"/album/" + albumData.forced_album} replace />
        <Footer />
      </>
    )
  } else {
    const availableAlbums = albumData.available_albums ?? []
    albumList = availableAlbums.map((albumName) => (
      <Link key={albumName} to={"/album/" + albumName} className={classes.albumLink}>
        <Card className={classes.card}>
          <Typography variant="h3" align="center" color="textPrimary" className={classes.albumLinkText} paragraph>
            {albumName}
          </Typography>
        </Card>
      </Link>
    ))
  }

  const handleClickOpen = () => {
    setDialogOpen(true);
  };

  const handleClose = () => {
    setDialogOpen(false);
  };

  return (
    <>
      <Header />
      <div className={classes.heroContent}>
        <Container maxWidth="sm">
          <Typography component="h1" variant="h2" align="center" color="textPrimary" gutterBottom>
            Welcome to CameraHub!
          </Typography>
          <Typography variant="h5" align="center" color="textSecondary" paragraph>
            You can use CameraHub to capture images or view already captured images. Choose one of the albums below or create a new album to start!
          </Typography>
        </Container>
      </div>
      <Container maxWidth="md" className={classes.albumCardContainer}>
        {albumList}
        <Card className={classes.card} onClick={handleClickOpen}>
          <Typography variant="h3" align="center" color="textPrimary" className={classes.albumLinkText} paragraph>
            Create new album
          </Typography>
        </Card>
      </Container>
      <NewAlbumDialog open={dialogOpen} handleClose={handleClose} />
      <Footer />
    </>
  );
};

export default FrontPage;
