import React from 'react';
import QrCodePage from './QrCodePage';
import LastImage from './LastImage';
import { useParams } from 'react-router-dom';

const QrCodeLastImagePage = () => {
  const { albumName } = useParams<{ albumName: string }>();
  return (
    <>
      <LastImage albumName={albumName} overlay={true} overlayTime={20000}/>
      <QrCodePage/>
    </>
  );
};

export default QrCodeLastImagePage
