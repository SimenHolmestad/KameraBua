[Back to readme](../README.md)

# Downloading images from the Raspberry PI
To download the images from the Raspberry PI, it is possible to use `scp` (secure copy). You could run the `scp` command from your own computer like this to get the images:

```
scp -r <username>@<ip_address>:<path_to_camera_hub>/CameraHub/backend/static/albums/<album_name> <location_on_your_computer>
```

For example, lets say you are in the following situation:

- Your Raspberry PI username is `pi`
- Your Raspberry PI is on the ip address `10.0.0.37`
- The CameraHub project is located in `~/projects` on the raspberry pi
- Your album is named `halloween`
- You want the album to be copied to `~/Documents/halloween` on your computer 

If this is the case, a possible `scp` command to download the images could be:

```
scp -r pi@10.0.0.37:~/projects/CameraHub/backend/static/albums/halloween ~/Documents/halloween
```

For more information on `scp`, see [this tutorial](https://linuxize.com/post/how-to-use-scp-command-to-securely-transfer-files/).
