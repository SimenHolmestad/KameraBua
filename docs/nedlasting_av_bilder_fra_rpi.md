[Tilbake til readme](../readme.md)

# Nedlasting av bilder fra Raspberry PI
For å laste ned bilder fra Raspberry PI kan du bruke `scp` (secure copy). Du kan kjøre `scp` fra din egen maskin slik for å hente bildene:

```
scp -r <brukernavn>@<ip_adresse>:<sti_til_camera_hub>/CameraHub/backend/static/albums/<album_navn> <plassering_pa_din_maskin>
```

For eksempel, la oss si at du er i følgende situasjon:

- Raspberry PI-brukernavnet ditt er `pi`
- Raspberry PI-en din har IP-adressen `10.0.0.37`
- CameraHub-prosjektet ligger i `~/projects` på Raspberry PI
- Albumet ditt heter `halloween`
- Du vil kopiere albumet til `~/Documents/halloween` på din maskin

I så fall kan en mulig `scp`-kommando se slik ut:

```
scp -r pi@10.0.0.37:~/projects/CameraHub/backend/static/albums/halloween ~/Documents/halloween
```

For mer informasjon om `scp`, se [denne veiledningen](https://linuxize.com/post/how-to-use-scp-command-to-securely-transfer-files/).

scp -r ./configs simen@10.0.0.26:~/CameraHub/configs
-i ~/.ssh/id_ed25519.pub
