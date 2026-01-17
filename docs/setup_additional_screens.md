[Back to readme](../README.md)

# Setup additional screens/monitors
CameraHub provides some "hidden pages" which are not accessible from the user interface. These pages are meant to be shown on a monitor or projector close to the camera. You as the Photoboth operator can choose which pages to be shown to the user.

**Note:** The urls shown in this documents are all meant to be placed behind the base-url which CameraHub is running on. E.g. if CameraHub is running on the url `10.0.0.13:5000`, the qr code page is found at:
```
http://10.0.0.13:5000/qr
```

## The qr code page
The qr code page shows the qr codes for the project and is found at:
```
/qr
```
If WiFi details are provided, this page will also show a QR-code for connecting to the WiFi network. See [show wifi code on main screen](show_wifi_qr_code_on_main_screen.md) for more information.
## The last image page
The last image page shows the last image captured to an album in fullscreen and is located at:
```
/album/<your_album_name>/last_image
```
The page will be updated every time a new image is added to the album.

The easiest way to access the last image page is to open a browser, navigate to the desired album page and add `/last_image` to the url.

## The slideshow page
The slideshow page shows a slideshow (in fullscreen) of the images in an album and can be accessed at:
```
/album/<your_album_name>/slideshow
```
The slideshow is continously updated as new images are added to the album. Having a slideshow on a seperate screen can be a nice addition to a photobooth.

# The last image qr page
The last image qr page is an extension to the [qr code page](#the-qr-code-page). The page looks just like the qr code page, but when a new image is captured to the album, the newly captured image is displayed in fullscreen for 20 seconds.

To access the page, go to:
```
/album/<your_album_name>/last_image_qr
```

# The slideshow last image page
The slideshow last image page shows a slideshow, but when a new image is captured to the album, the newly captured image is displayed for 20 seconds. The slideshow last image page can be found at:
```
/album/<your_album_name>/slideshow_last_image
```
