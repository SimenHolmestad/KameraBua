[Back to readme](../README.md)

# Possible Improvements to CameraHub
There are probably a lot more improvements than these, but these are some I have been thinking about:

## Using websockets instead of polling server
Currently, the info screens need to continuously poll the server to check for updates. This process could probably have been better with websockets.

## Configuration file improvements
Now that the app uses a single config file, it could be extended with more options (for example how long an image should be displayed on a screen/monitor before disappearing).

## Better testing of the scripts/commands
Most of these are not very well tested as of now.

# History and goals of CameraHub
CameraHub is partly made as a rewamping of [this project](https://github.com/SimenHolmestad/Fotobox) made some time ago, but aims to:

- Be more modular
- Be easier to extend
- Provide more functionality
- Be easier to setup and maintain
- Be more lightweight
- Provide a better user experience
