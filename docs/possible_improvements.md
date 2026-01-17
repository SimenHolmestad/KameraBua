[Back to readme](../README.md)

# Possible Improvements to CameraHub
There are probably a lot more improvements than these, but these are some I have been thinking about:

## Using websockets instead of polling server
Currently, the info screens need to continuously poll the server to check for updates. This process could probably have been better with websockets.

## Configuration files instead of command line arguments
Right now the WiFi QR code system needs to be configured with a json file while the rest of the system needs to be configured with command line arguments. Maybe it would be better to have it all in a single configuration file? In the configuration file, all the possible options can also be written out as comments and it is possible to allow for more configurations. (like how many seconds an image should be displayed on a screen/monitor before disappearing).

## Better testing of the scripts/run_commands
Most of these are not very well tested as of now.

# History and goals of CameraHub
CameraHub is partly made as a rewamping of [this project](https://github.com/SimenHolmestad/Fotobox) made some time ago, but aims to:

- Be more modular
- Be easier to extend
- Provide more functionality
- Be easier to setup and maintain
- Be more lightweight
- Provide a better user experience
