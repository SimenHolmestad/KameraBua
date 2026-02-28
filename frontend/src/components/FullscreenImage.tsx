import React from 'react';
import { makeStyles } from '@mui/styles';
import type { Theme } from '@mui/material/styles';

type StyleProps = {
  opacity: number;
};

const useStyles = makeStyles<Theme, StyleProps>(({
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
    opacity: (props) => props.opacity
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
    opacity: (props) => props.opacity
  }
}))

type FullscreenImageProps = {
  imageUrl?: string | null;
  time?: number;
  startHided?: boolean;
};

const FullscreenImage = ({ imageUrl, time, startHided }: FullscreenImageProps) => {
  const [extraStyles, setExtraStyles] = React.useState<StyleProps>({ opacity: 0 });
  let firstImageShowing = React.useRef(true);
  const [isShowing, setIsShowing] = React.useState(false);
  const classes = useStyles(extraStyles);
  let timeout = React.useRef<ReturnType<typeof setTimeout> | null>(null)

  React.useEffect(() => {
    if (!imageUrl) {
      return
    }
    if (startHided && firstImageShowing.current) {
      firstImageShowing.current = false
      return
    }

    setExtraStyles({opacity: 1})
    setIsShowing(true)

    if (timeout.current) {
      clearTimeout(timeout.current)
    }
    if (time) {
      timeout.current = setTimeout(startFadeOut, time)
    }
  }, [imageUrl, startHided, time]);

  const startFadeOut = () => {
    setExtraStyles({opacity: 0})
    timeout.current = setTimeout(() => setIsShowing(false), 1000);
  }

  if (!isShowing) {
    return null;
  }

  return (
    <div className={ classes.background }>
      <img src={imageUrl} className={ classes.image } alt=""/>
    </div>
  );
};

export default FullscreenImage
