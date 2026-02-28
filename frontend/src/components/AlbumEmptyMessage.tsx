import React from 'react';
import { makeStyles } from '@mui/styles';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

const useStyles = makeStyles(() => ({
  noImagesDiv: {
    height: "90vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center"
  },
  emptyAlbumText: {
    fontWeight: "200"
  }
}));

const AlbumEmptyMessage = () => {
  const classes = useStyles();
  return (
    <div className={ classes.noImagesDiv }>
      <Container maxWidth="sm">
        <Typography variant="h3" className={classes.emptyAlbumText} align="center" color="textSecondary" gutterBottom>
          There are no images
        </Typography>
        <Typography variant="h5" className={classes.emptyAlbumText} align="center" color="textSecondary" paragraph>
          There are currently no images in this album. Images will appear here when they are captured to the album.
        </Typography>
      </Container>
    </div>
  );
};

export default AlbumEmptyMessage
