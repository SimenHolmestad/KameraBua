import React from 'react';
import SlideshowPage from './SlideshowPage';
import LastImage from './LastImage';
import { useParams } from 'react-router-dom';

const SlideshowLastImagePage = () => {
  const { albumName } = useParams();
  return (
    <>
      <SlideshowPage />
      <LastImage albumName={albumName} overlay={true} overlayTime={20000}/>
    </>
  );
};

export default SlideshowLastImagePage
