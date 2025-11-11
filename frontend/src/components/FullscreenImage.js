import React from 'react';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles(({
  image: {
    maxWidth: "100%",
    maxHeight: "100%",
    bottom: "0",
    left: "0",
    margin: "auto",
    position: "fixed",
    right: "0",
    top: "0",
    objectFit: "contain",
    zoom: 10,
    transition: "opacity 1s ease-in-out",
    opacity: props => props.opacity
  },
  background: {
    position: "fixed",
    zIndex: 1200,
    top: 0,
    left: 0,
    width: "100%",
    height:" 100%",
    backgroundColor: "black",
    transition: "opacity 1s ease-in-out",
    opacity: props => props.opacity
  }
}))

const FullscreenImage = (props) => {
  const [extraStyles, setExtraStyles] = React.useState({ opacity: 0 });
  let firstImageShowing = React.useRef(true);
  const [isShowing, setIsShowing] = React.useState(false);
  const classes = useStyles(extraStyles);
  let timeout = React.useRef(null)

  React.useEffect(() => {
    if (!props.imageUrl) {
      return
    }
    if (props.startHided && firstImageShowing.current) {
      firstImageShowing.current = false
      return
    }

    setExtraStyles({opacity: 1})
    setIsShowing(true)

    clearTimeout(timeout.current)
    if (props.time) {
      timeout.current = setTimeout(StartFadeOut, props.time)
    }
  }, [props]);

  const StartFadeOut = () => {
    setExtraStyles({opacity: 0})
    timeout.current = setTimeout(() => setIsShowing(false), 1000);
  }

  if (!isShowing) {
    return null;
  }

  return (
    <div className={ classes.background }>
      <img src={props.imageUrl} className={ classes.image } alt=""/>
    </div>
  );
};

export default FullscreenImage
