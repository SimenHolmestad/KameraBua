import React, { useState, useEffect } from 'react';
import { get_album_info, isApiError } from './../server'
import AlbumOverview from './AlbumOverview'
import ImageDetail from './ImageDetail'
import CircularProgress from '@mui/material/CircularProgress';
import { makeStyles } from '@mui/styles';
import Grid from '@mui/material/Grid';
import Header from './Header';
import { useParams } from 'react-router-dom';
import Footer from './Footer';
import type { Theme } from '@mui/material/styles';
import type { AlbumInfoResponse } from '../api';

const useStyles = makeStyles((theme: Theme) => ({
  loadingGrid: {
    height: "80vh",
    paddingTop: "250px",
  }
}));

type AlbumPageView = 'detail' | 'overview';

type AlbumPageProps = {
  view?: AlbumPageView;
};

const AlbumPage = ({ view = 'overview' }: AlbumPageProps) => {
  const { albumName } = useParams<{ albumName: string }>();
  const [albumData, setAlbumData] = useState<AlbumInfoResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [imageIndex, setImageIndex] = React.useState(1);
  const info_gather_interval = React.useRef<ReturnType<typeof setInterval> | null>(null)
  const classes = useStyles();

  // Update the album data from server every 5 seconds
  useEffect(() => {
    if (!albumName) {
      setErrorMessage("Album name is missing.");
      return;
    }

    const gather_album_data = async () => {
      const albumInfo = await get_album_info(albumName)
      if (isApiError(albumInfo)) {
        setErrorMessage(albumInfo.error)
        if (info_gather_interval.current) {
          clearInterval(info_gather_interval.current)
        }
        return;
      }
      setErrorMessage(null);
      setAlbumData(albumInfo);
      console.log(albumInfo);
    }

    gather_album_data()
    info_gather_interval.current = setInterval(gather_album_data, 5000);
    return () => {
      if (info_gather_interval.current) {
        clearInterval(info_gather_interval.current);
      }
    };
  }, [albumName]);

  if (errorMessage) {
    return (
      <>
        <Header />
        <h1>ERROR: {errorMessage}</h1>
        <Footer />
      </>
    )
  }

  if (!albumData) {
    return (
      <>
        <Header />
        <Grid container className={classes.loadingGrid} spacing={2} justifyContent="center">
          <CircularProgress />
        </Grid>
        <Footer />
      </>
    )
  }

  const safeAlbumName = albumName ?? "";

  const imageDetail = (
    <ImageDetail
      imageUrls={albumData.image_urls}
      imageIndex={imageIndex}
      setImageIndex={setImageIndex}
      albumName={safeAlbumName} />
  )

  const albumOverview = (
    <AlbumOverview
      albumData={albumData}
      setAlbumData={setAlbumData}
      setImageIndex={setImageIndex} />
  );

  const pageContent = view === 'detail' ? imageDetail : albumOverview;

  return (
    <>
      <Header />
      {pageContent}
      <Footer />
    </>
  )
};

export default AlbumPage
