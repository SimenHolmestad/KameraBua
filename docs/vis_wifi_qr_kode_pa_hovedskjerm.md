[Tilbake til readme](../readme.md)

# Vis WiFi-kode på skjerm
Hvis du vet at noen (eller alle) av photobooth-brukerne ikke er koblet til WiFi-nettverket ditt, kan det være lurt å gi dem en QR-kode for å koble seg til. Å lage en slik QR-kode kan gjøres enkelt med CameraHub.

For å lage en WiFi-QR-kode må du først konfigurere WiFi-innstillingene i `.env`. Sett følgende variabler:

```
CAMERAHUB_WIFI_QR_CODE__ENABLED=true
CAMERAHUB_WIFI_QR_CODE__WIFI_NAME=my_wifi_SSID
CAMERAHUB_WIFI_QR_CODE__PROTOCOL=WPA/WPA2
CAMERAHUB_WIFI_QR_CODE__PASSWORD=my_super_secret_password
CAMERAHUB_WIFI_QR_CODE__DESCRIPTION=Scan qr code to connect to my_wifi_SSID!
```

Etter at du har oppdatert `.env`, kjør eller deploy applikasjonen på nytt for at WiFi-QR-koden skal bli generert og vist på skjermen. QR-koden lagres på `backend/static/qr_codes/wifi_qr_code.png`.

**Advarsel:** Passordet til nettverket lagres i klartekst i QR-koden, noe som kan være uheldig avhengig av situasjonen din.
