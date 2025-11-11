import React from 'react';
import FullscreenImage from './FullscreenImage';


const Slideshow = ({ imageUrls }) => {
  const [topImageIndex, setTopImageIndex] = React.useState(0);
  const [bottomImageIndex, setBottomImageIndex] = React.useState(1 % imageUrls.length);
  const bottomImageRef = React.useRef(1 % imageUrls.length);
  const numberOfImagesRef = React.useRef(imageUrls.length);
  const topImageShowing = React.useRef(false);

  React.useEffect(() => {
    numberOfImagesRef.current = imageUrls.length
  }, [imageUrls]);

  React.useEffect(() => {
    const interval = setInterval(() => {
      const currentValue = bottomImageRef.current
      let nextValue = Math.floor(Math.random() * numberOfImagesRef.current)
      if (currentValue === nextValue) {
        nextValue = (nextValue + 1) % numberOfImagesRef.current
      }

      topImageShowing.current = true
      setTopImageIndex(currentValue)
      setTimeout(() => {
        bottomImageRef.current = nextValue
        setBottomImageIndex(nextValue)
      }, 1000)
      setTimeout(() => {
        topImageShowing.current = false
      }, 3000)
    }, 8000);
    return () => clearInterval(interval);
  }, []);

  let topImage = null
  if (topImageShowing.current) {
    topImage = <FullscreenImage imageUrl={ imageUrls[topImageIndex] } time={ 2000 }/>
  }

  return (
    <>
      <FullscreenImage imageUrl={ imageUrls[bottomImageIndex] }/>
      { topImage }
    </>
  );
};

export default Slideshow
