import React from 'react';
import { get_last_image_url, isApiError } from './../server'
import CircularProgress from '@mui/material/CircularProgress';
import FullscreenImage from './FullscreenImage';
import AlbumEmptyMessage from './AlbumEmptyMessage';

type LastImageProps = {
  albumName?: string;
  overlay?: boolean;
  overlayTime?: number;
};

const LastImage = ({ albumName, overlay = false, overlayTime }: LastImageProps) => {
  const [imageUrl, setImageUrl] = React.useState<string | null>(null);
  const [albumEmpty, setAlbumEmpty] = React.useState(false);
  const [albumExists, setAlbumExists] = React.useState(true);

  React.useEffect(() => {
    const getLastImageData = () => {
      if (!albumName) {
        setAlbumExists(false);
        return;
      }
      get_last_image_url(albumName).then((data) => {
        if (isApiError(data)) {
          if (data.error === "album is empty") {
            setAlbumEmpty(true)
            return;
          }
          setAlbumExists(false)
          return;
        }
        setImageUrl(data.last_image_url);
        setAlbumEmpty(false)
        setAlbumExists(true)
      });
    }

    if (!albumName) {
      setAlbumExists(false);
      return;
    }

    getLastImageData()
    const interval = setInterval(getLastImageData, 1500);
    return () => clearInterval(interval);
  }, [albumName]);

  if (!albumExists) {
    return <h1>There is no album named {albumName}</h1>
  }

  if (albumEmpty && !overlay) {
    return <AlbumEmptyMessage/>
  }

  if (!imageUrl && !overlay) {
    return <CircularProgress/>
  }

  if (!imageUrl) {
    return null;
  }

  return (
    <FullscreenImage imageUrl={ imageUrl } time={ overlayTime } startHided={ overlay }/>
  );
};

export default LastImage
