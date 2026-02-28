import React from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import AlbumEmptyMessage from './AlbumEmptyMessage';
import Slideshow from './Slideshow';
import { get_album_info, isApiError } from './../server'
import { useParams } from 'react-router-dom';


const SlideshowPage = () => {
  const [imageUrls, setImageUrls] = React.useState<string[] | null>(null);
  const [errorMessage, setErrorMessage] = React.useState<string | null>(null);
  const { albumName } = useParams<{ albumName: string }>();

  // Update the album data from server every 30 seconds
  React.useEffect(() => {
    if (!albumName) {
      setErrorMessage("Album name is missing.");
      return;
    }

    get_album_info(albumName).then((data) => {
      if (isApiError(data)) {
        setErrorMessage(data.error);
        return;
      }
      setErrorMessage(null);
      setImageUrls(data.image_urls);
    });
    const interval = setInterval(() => {
      get_album_info(albumName).then((data) => {
        if (isApiError(data)) {
          setErrorMessage(data.error);
          return;
        }
        setErrorMessage(null);
        setImageUrls(data.image_urls);
      });
    }, 30000);
    return () => clearInterval(interval);
  }, [albumName]);

  if (errorMessage) {
    return <h1>ERROR: {errorMessage}</h1>
  }

  if (imageUrls === null) {
    return <CircularProgress/>
  }

  if (imageUrls.length === 0) {
    return <AlbumEmptyMessage/>
  }

  return (
    <Slideshow imageUrls={imageUrls}/>
  );
};

export default SlideshowPage
