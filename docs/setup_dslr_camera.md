[Back to readme](../README.md)

# Prerequisites
Before setting up CameraHub on your Raspberry PI with a DSLR camera, you should first read through [the guide on how to setup CameraHub on the Raspberry PI](setup_with_raspberry_pi.md).

# Setting up CameraHub with a DSLR Camera
To use CameraHub with a DSLR Camera, you need to use one of the DSLR camera modules. These modules all rely on the gphoto2 library. The easiest way to install gphoto2 for Raspberry PI seems to be the command:
```
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh
```
Which can be found in <https://github.com/gonzalo/gphoto2-updater>.

After installing gphoto2 you need to install the gphoto2 python package by doing:
```
pip3 install gphoto2
```

After installing gphoto2, you can connect your DSLR camera to the Raspberry PI via USB and run the application as described in the [setup guide for Raspberry PI](setup_with_raspberry_pi.md)

# The upsides and downsides of the DSLR Modules

Currently, CameraHub has three different dslr modules with their upsides and downsides. The modules, sorted by speed from fastest to slowest, are as follows:
- The dslr jpg module
- The dslr raw module
- The dlsr raw transfer module

The `dlsr raw transfer module` is the best choice (if you want raw images) but also uses the most time.

**NOTE**: The Camera modules currently only work with Canon cameras. If you want to use cameras of other types, some rewriting must be done.

The DSLR camera modules are described below:
## The dslr jpg module
If you do not want to keep the raw images from the camera, this is definitely the best option as it is the fastest (a little below 2 seconds per image capture on a Canon EOS 6D)

Be carefaul however: Your camera needs to be set to save .jpg images (and .jpg images only!) for this to work.

## The dslr raw module
With the dslr raw module, the raw image is kept on the SD card of the camera while the .jpg image is transferred to the Raspberry PI.

When testing on my Canon EOS 6D, this module used around 4 seconds per image capture.

Note: When using the raw modules, the dslr must be set to save the images as *both* .jpg and raw.

## The dlsr raw transfer module
With the DLSR raw transfer module, both the raw images and the .jpg images are transferred from the camera to the Raspberry PI.

When testing on my Canon EOS 6D, the dslr raw transfer module used between 5 and 6 seconds per image capture.

One of the reasons you might want your raw images transferred to the Raspberry PI is that the images will be sorted by album. This will not be the case for the dslr raw module.
