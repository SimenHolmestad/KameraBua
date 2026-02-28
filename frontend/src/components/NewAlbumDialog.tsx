import React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { create_or_update_album, isApiError } from './../server'
import { Navigate } from "react-router-dom";
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';

type NewAlbumDialogProps = {
  open: boolean;
  handleClose: () => void;
};

const NewAlbumDialog = ({ open, handleClose }: NewAlbumDialogProps) => {
  const [albumName, setAlbumName] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [redirectAlbum, setRedirectAlbum] = React.useState<string | null>(null);
  const [errorMessage, setErrorMessage] = React.useState<string | null>(null);
  const handleDialogClose = () => {
    setErrorMessage(null);
    handleClose();
  };

  const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const response = await create_or_update_album(albumName, description)
    if (isApiError(response)) {
      setErrorMessage(response.error);
      return;
    }
    setRedirectAlbum(response.album_name)
  };

  if (redirectAlbum) {
    return <Navigate to={"/album/" + redirectAlbum} replace />
  }

  return (
    <div>
      <Dialog open={open} onClose={handleDialogClose}>
        <DialogTitle>Create new album</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Every image stored in CameraHub must be connected to an album. Please enter a name and description for your new album below.
          </DialogContentText>
          <TextField
            value={albumName}
            onChange={e => setAlbumName(e.target.value)}
            autoFocus
            margin="dense"
            label="Album name"
            fullWidth
          />
          <TextField
            value={description}
            onChange={e => setDescription(e.target.value)}
            label="Description"
            multiline
            rows={4}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleSubmit} color="primary">
            Create album
          </Button>
        </DialogActions>
      </Dialog>
      <Snackbar
        open={Boolean(errorMessage)}
        autoHideDuration={5000}
        onClose={() => setErrorMessage(null)}
      >
        <Alert severity="error" variant="filled" elevation={6}>
          {errorMessage}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default NewAlbumDialog
