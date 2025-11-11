import React from 'react';
import { makeStyles } from '@mui/styles';
import ArrowBack from '@mui/icons-material/ArrowBack';
import ArrowForward from '@mui/icons-material/ArrowForward';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import CircularProgress from '@mui/material/CircularProgress';
import { Link } from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  leftIcon: {
    marginRight: theme.spacing(1),
  },
  rightIcon: {
    marginLeft: theme.spacing(1),
  },
  image: {
    width: "100%"
  },
  imageContainer: {
    maxWidth: "1100px",
    padding: theme.spacing(0, 0, 0),
  },
  backToAlbumButton: {
    marginTop: "4px"
  },
}));

const ImageDetail = ({imageUrls, imageIndex, setImageIndex, albumName}) => {
  const classes = useStyles();
  const [leftIsLoading, setLeftIsLoading] = React.useState(false);
  const [rightIsLoading, setRightIsLoading] = React.useState(false);

  const goToNextImage = () => {
    if (imageIndex > 1) {
      setImageIndex(imageIndex - 1)
      setRightIsLoading(true)
    }
  }

  const goToPreviousImage = () => {
    if (imageIndex < imageUrls.length) {
      setImageIndex(imageIndex + 1)
      setLeftIsLoading(true)
    }
  }

  const doneLoading = () => {
    setLeftIsLoading(false)
    setRightIsLoading(false)
  }

  const leftButtonDisabled = imageIndex >= imageUrls.length
  const rightButtonDisabled = imageIndex <= 1

  let leftButton = null
  if (leftIsLoading) {
    leftButton = <CircularProgress size="2em"/>
  } else {
    leftButton = (
      <Button onClick={goToPreviousImage} disabled={leftButtonDisabled}>
        <ArrowBack className={classes.leftIcon} />
        Previous image
      </Button>
    )
  }

  let rightButton = null
  if (rightIsLoading) {
    rightButton = <CircularProgress size="2em"/>
  } else {
    rightButton = (
      <Button onClick={goToNextImage} disabled={rightButtonDisabled}>
        Next image
        <ArrowForward className={classes.rightIcon} />
      </Button>
    )
  }

  return (
    <>
      <Container className={classes.imageContainer}>
        <Button component={Link} to={"/album/" + albumName} className={classes.backToAlbumButton}>
          <KeyboardArrowLeft />
          Back to album
        </Button>
        <img className={classes.image}
             onLoad={doneLoading}
             src={imageUrls[imageUrls.length - imageIndex]}
             alt=""/>
        <Grid container justifyContent="space-between">
          {leftButton}
          {rightButton}
        </Grid>
      </Container>
    </>
  );
};

export default ImageDetail
