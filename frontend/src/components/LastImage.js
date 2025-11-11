import React from 'react';
import { get_last_image_url } from './../server'
import CircularProgress from '@mui/material/CircularProgress';
import FullscreenImage from './FullscreenImage';
import AlbumEmptyMessage from './AlbumEmptyMessage';

const LastImage = (props) => {
  const [imageUrl, setImageUrl] = React.useState(null);
  const [albumEmpty, setAlbumEmpty] = React.useState(false);
  const [albumExists, setAlbumExists] = React.useState(true);
  const albumName = props.albumName;

  React.useEffect(() => {
    const getLastImageData = () => {
      get_last_image_url(albumName).then((data) => {
        if (data["error"] && data["error"] === "album is empty") {
          setAlbumEmpty(true)
        } else if (data["error"]) {
          setAlbumExists(false)
        } else {
          setImageUrl(data["last_image_url"]);
          setAlbumEmpty(false)
        }
      });
    }

    getLastImageData()
    const interval = setInterval(getLastImageData, 1500);
    return () => clearInterval(interval);
  }, [albumName]);

  if (!albumExists) {
    return <h1>There is no album named {albumName}</h1>
  }

  if (albumEmpty && !props.overlay) {
    return <AlbumEmptyMessage/>
  }

  if (!imageUrl && !props.overlay) {
    return <CircularProgress/>
  }

  return (
    <FullscreenImage imageUrl={ imageUrl } time={ props.overlayTime } startHided={ props.overlay }/>
  );
};

export default LastImage
