import React from 'react';
import { get_qr_codes, isApiError } from './../server';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import { makeStyles } from '@mui/styles';
import Header from './Header';
import type { Theme } from '@mui/material/styles';
import type { GetQrCodesQrCodesGetResponses } from '../api';

const useStyles = makeStyles((theme: Theme) => ({
  qrCodeGridItem: {
    width: "45%"
  },
  qrCodeGrid: {
    width: "100%"
  },
  image: {
    width: "100%"
  },
  verticallyCenteredDiv: {
    height: "90vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center"
  }
}));

type QrCodeResponse = GetQrCodesQrCodesGetResponses[200];

const QrCodePage = () => {
  const classes = useStyles();
  const [qrCodeData, setQrCodeData] = React.useState<QrCodeResponse["qr_codes"]>([]);
  const [errorMessage, setErrorMessage] = React.useState<string | null>(null);
  React.useEffect(() => {
    const fetchData = async () => {
      const response = await get_qr_codes()
      if (isApiError(response)) {
        setErrorMessage(response.error);
        return;
      }
      setQrCodeData(response.qr_codes)
    }
    fetchData()
  }, []);

  const qrCodes = qrCodeData.map((qrCode, index) => (
    <Grid item key={index} className={classes.qrCodeGridItem}>
      <img className={classes.image}
           src={qrCode.url}
           alt={qrCode.name}/>
      <Typography variant="h6" align="center">
        {qrCode.information}
      </Typography>
    </Grid>
  ))

  return (
    <>
      <Header/>
      <div className={classes.verticallyCenteredDiv}>
        <Grid container justifyContent="space-around" className={classes.qrCodeGrid}>
          {errorMessage ? (
            <Typography variant="h6" align="center" color="error">
              {errorMessage}
            </Typography>
          ) : (
            qrCodes
          )}
        </Grid>
      </div>
    </>
  );
};

export default QrCodePage
