import React from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import AlbumEmptyMessage from './AlbumEmptyMessage';
import Slideshow from './Slideshow';
import { get_album_info } from './../server'
import { useParams } from 'react-router-dom';


const SlideshowPage = () => {
  const [imageUrls, setImageUrls] = React.useState(null);
  const { albumName } = useParams();

  // Update the album data from server every 30 seconds
  React.useEffect(() => {
    get_album_info(albumName).then((data) => {
      setImageUrls(data.image_urls);
    });
    const interval = setInterval(() => {
      get_album_info(albumName).then((data) => {
        setImageUrls(data.image_urls);
      });
    }, 30000);
    return () => clearInterval(interval);
  }, [albumName]);

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
