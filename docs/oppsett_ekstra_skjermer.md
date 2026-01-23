[Tilbake til readme](../readme.md)

# Oppsett av ekstra skjermer/monitorer
CameraHub tilbyr noen "skjulte sider" som ikke er tilgjengelige fra brukergrensesnittet. Disse sidene er ment å vises på en skjerm eller prosjektor nær kameraet. Du som photobooth-operator kan velge hvilke sider som skal vises til brukerne.

**Merk:** URL-ene i dette dokumentet skal legges bak base-URL-en som CameraHub kjører på. For eksempel, hvis CameraHub kjører på `10.0.0.13:5000`, finner du QR-kodesiden på:
```
http://10.0.0.13:5000/qr
```

## QR-kodesiden
QR-kodesiden viser QR-kodene for prosjektet og finnes på:
```
/qr
```
Hvis WiFi-detaljer er angitt, vil denne siden også vise en QR-kode for å koble til WiFi-nettverket. Se [vis WiFi QR-kode på hovedskjerm](vis_wifi_qr_kode_pa_hovedskjerm.md) for mer informasjon.

## Siden for siste bilde
Siden for siste bilde viser det siste bildet som er tatt til et album i fullskjerm, og finnes på:
```
/album/<ditt_album_navn>/last_image
```
Siden oppdateres hver gang et nytt bilde legges til albumet.

Den enkleste måten å åpne siden på er å gå til ønsket albumside i nettleseren og legge til `/last_image` i URL-en.

## Lysbildefremvisning
Siden for lysbildefremvisning viser en slideshow (i fullskjerm) av bildene i et album, og nås på:
```
/album/<ditt_album_navn>/slideshow
```
Lysbildefremvisningen oppdateres kontinuerlig når nye bilder legges til. Å ha en slideshow på en egen skjerm kan være et fint tillegg til en photobooth.

# Siden for siste bilde + QR
Siden for siste bilde + QR er en utvidelse av [QR-kodesiden](#qr-kodesiden). Siden ser ut som QR-kodesiden, men når et nytt bilde tas til albumet, vises det nyeste bildet i fullskjerm i 20 sekunder.

For å åpne siden, gå til:
```
/album/<ditt_album_navn>/last_image_qr
```

# Siden for slideshow + siste bilde
Siden for slideshow + siste bilde viser en slideshow, men når et nytt bilde tas til albumet, vises det nyeste bildet i 20 sekunder. Denne siden finnes på:
```
/album/<ditt_album_navn>/slideshow_last_image
```
