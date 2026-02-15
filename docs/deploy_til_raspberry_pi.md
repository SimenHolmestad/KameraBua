# Kjør applikasjonen

## Lag en .env-fil

Du finner en eksempel fil [her](../.env.example).
Formatet på innstillinger kan finnes [her](../backend/core/config.py).

Det kan være fint å redigere .env-filen lokalt på maskinen og gjøre følgende for å kopiere til RPI:
```
scp ./.env <brukernavn>@<ip-adresse>:~/CameraHub/.env
```

Deretter kan man kjøre med:
```
ssh <brukernavn>@<ip-adresse>
cd ~/CameraHub
source .venv/bin/activate
sudo .venv/bin/python -m scripts.deploy --env-file ./.env
```

Man kan også redeploye med:
```
sudo .venv/bin/python -m scripts.update_and_redeploy --env-file ./.env
```

# Neste steg
- [Oppsett av ekstra skjermer/monitorer](oppsett_ekstra_skjermer.md)
- [Vis WiFi QR-kode på hovedskjerm](vis_wifi_qr_kode_pa_hovedskjerm.md)
- [Oppsett av speilreflekskamera](oppsett_dslr_kamera.md)
- [Nedlasting av bilder fra Raspberry PI](nedlasting_av_bilder_fra_rpi.md)
- [Utvikling på Raspberry PI](utvkling_paa_raspberry_pi.md)
