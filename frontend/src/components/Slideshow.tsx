import React from 'react';
import FullscreenImage from './FullscreenImage';


type SlideshowProps = {
  imageUrls: string[];
};

const Slideshow = ({ imageUrls }: SlideshowProps) => {
  const safeLength = Math.max(imageUrls.length, 1);
  const [topImageIndex, setTopImageIndex] = React.useState(0);
  const [bottomImageIndex, setBottomImageIndex] = React.useState(1 % safeLength);
  const bottomImageRef = React.useRef(1 % safeLength);
  const numberOfImagesRef = React.useRef(imageUrls.length);
  const topImageShowing = React.useRef(false);

  React.useEffect(() => {
    numberOfImagesRef.current = imageUrls.length
    if (imageUrls.length <= 1) {
      setTopImageIndex(0);
      setBottomImageIndex(0);
      bottomImageRef.current = 0;
    }
  }, [imageUrls]);

  React.useEffect(() => {
    if (imageUrls.length <= 1) {
      return;
    }
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
  }, [imageUrls.length]);

  if (imageUrls.length === 0) {
    return null;
  }

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
