import React from 'react';
import LastImage from './LastImage'
import { useParams } from 'react-router-dom';

const LastImagePage = () => {
  const { albumName } = useParams<{ albumName: string }>();
  return (
    <LastImage albumName={albumName}/>
  );
};

export default LastImagePage
