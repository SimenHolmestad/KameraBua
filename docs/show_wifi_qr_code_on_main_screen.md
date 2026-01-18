[Back to readme](../README.md)

# Show WiFi-code on screen
If you know some (or all) of your photobooth users will not be connected to the your WiFi network, it might be a good idea to provide the users with a QR code to connect to the WiFi. Creating such a QR code can be accomplished quite easily with the CameraHub system.

To create a WiFi QR code you must first configure the WiFi settings in `config/config.json` under the `qr_codes.wifi` section. The config should be on the following format:

```
{
  "enabled": true,
  "name": "my_wifi_SSID",
  "protocol": "WPA/WPA2",
  "password": "my_super_secret_password",
  "description": "Scan qr code to connect to my_wifi_SSID!"
}
```

After updating `config/config.json`, run or deploy the application (again) for the WiFi QR Code to be created and shown on screen. The WiFi QR code will be saved with the file path `backend/static/qr_codes/wifi_qr_code.png`.

**Warning:** The password of your network will be stored in plaintext inside the WiFi QR code, which might not be ideal depending on your situation.
