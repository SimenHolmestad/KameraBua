[Back to readme](../README.md)

# Setting up CameraHub on the Raspberry PI
CameraHub is meant to be run on a Raspberry Pi (or RPI or simply PI for short). To set up CameraHub on the Raspberry PI, it is recommended to have some experience with ssh and running commands in the terminal.

The recommended way of setting up CameraHub on the RPI is provided below, but some of the steps might be done in other ways. If you already have your Raspberry set up, you can move to the section [install project dependencies](#install-project-dependencies).

## Installing the Raspberry PI OS
To install an operating system on the Raspberry PI, do the following:
1. Download the OS ([Raspberry Pi OS with desktop](https://www.raspberrypi.org/software/operating-systems/) is recommended)
2. Write the OS to the Micro SD card by using [balena etcher](https://www.balena.io/etcher/)
3. (Optional) Write WiFi-information to the SD card (see [this guide](https://www.raspberrypi.org/documentation/remote-access/README.md))
4. Put the Micro SD card into the RPI

Writing WiFi-information to the Raspberry PI is only needed if you want connect to the PI using WiFi (not cable) and you do not want to connect the Raspberry PI to a keyboard and mouse.

## Connecting to the Raspberry PI
It is possible to run CameraHub directly on the Raspberry PI with a keyboard and mouse connected to it. I find it however better to connect to it using SSH.

To connect to the PI using SSH, you first have to make sure the PI is connected to your network (if on wifi, you can follow [this guide](https://www.raspberrypi.org/documentation/configuration/wireless/README.md)). When the PI is connected to the network, check out [this guide](https://www.raspberrypi.org/documentation/remote-access/README.md) on accessing it using SSH.

**NOTE:** The Raspberry PI needs to be connected to the same network as the units which are going to access the CameraHub application.

## Installing project dependencies
In the RPI terminal, make sure that node and npm are installed by doing:
```
sudo apt-get install nodejs npm
```
Then, download the project and install python requirements by doing:
```
git clone https://github.com/SimenHolmestad/CameraHub.git
cd CameraHub
pip3 install -r python-requirements.txt
```

Note that using a DSLR camera requires [further installation steps](#the-dslr-camera-modules).

# Running the application (Not deploying!)
The command for running the application on the Raspberry PI is:
```
python3 -m scripts
```

To use an actual camera, set `camera.module` in `config/config.json` to one of:

- `rpicam` (for Raspberry Pi Camera Module)
- `dslr_jpg`
- `dslr_raw`
- `dslr_raw_transfer`
- `dummmy` (default)

It is also possible to run the application with access to only a single album. To do this, set `albums.forced_album` in `config/config.json`.

With the users only being able to access to a single album, the user interface becomes simpler.

If you for example want to run CameraHub using the Raspberry PI Camera Module and have just one album named "Halloween", your config should include:

```
{
  "albums": {
    "forced_album": "Halloween"
  },
  "camera": {
    "module": "rpicam",
    "options": {}
  },
  "qr_codes": {
    "use_center_images": true,
    "wifi": {
      "enabled": false,
      "name": "",
      "protocol": "",
      "password": "",
      "description": ""
    }
  }
}
```

# Deploying
As we want CameraHub to run at all times, we need to deploy it somehow. One way to deploy the application is to use systemd, as described in [this blog post](https://blog.miguelgrinberg.com/post/running-a-flask-application-as-a-service-with-systemd). To make depoying to systemd simpler, a deploy script is provided to do this job. To deploy, run:

```
sudo python3 -m scripts.deploy
```

To redeploy with other settings, update `config/config.json` and run the deploy command again.

If you want to get the status of the system after deploying, you can run the command:
```
sudo systemctl status camerahub
```

# Next steps
- [Setting up additional screens/monitors](setup_additional_screens.md)
- [Create a WiFi QR code to show on screen](show_wifi_qr_code_on_main_screen.md)
- [Setup DSLR camera](setup_dslr_camera.md) (if desired)
- [Download images from the Raspberry PI](downloading_images_from_the_rpi.md)
