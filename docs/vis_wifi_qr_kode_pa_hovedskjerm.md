[Tilbake til readme](../readme.md)

# Vis WiFi-kode på skjerm
Hvis du vet at noen (eller alle) av photobooth-brukerne ikke er koblet til WiFi-nettverket ditt, kan det være lurt å gi dem en QR-kode for å koble seg til. Å lage en slik QR-kode kan gjøres enkelt med CameraHub.

For å lage en WiFi-QR-kode må du først konfigurere WiFi-innstillingene i `configs/config.json` under `wifi_qr_code`. Configen skal ha følgende format:

```
{
  "enabled": true,
  "wifi_name": "my_wifi_SSID",
  "protocol": "WPA/WPA2",
  "password": "my_super_secret_password",
  "description": "Scan qr code to connect to my_wifi_SSID!"
}
```

Etter at du har oppdatert `configs/config.json`, kjør eller deploy applikasjonen på nytt for at WiFi-QR-koden skal bli generert og vist på skjermen. QR-koden lagres på `backend/static/qr_codes/wifi_qr_code.png`.

**Advarsel:** Passordet til nettverket lagres i klartekst i QR-koden, noe som kan være uheldig avhengig av situasjonen din.
