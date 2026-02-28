[Tilbake til readme](../readme.md)

# Lokal utvikling
Under utvikling vil applikasjonen lage bilder som dette når det ikke er noe kamera koblet til:

![Dummy demo circle image](images/dummy_demo_image.png)

# Installering av avhengigheter
Du trenger `gphoto2` for a kunne bruke applikasjonen med speilreflekskamera. Appen laster ned bildet den skal bruke, mens raw-filen blir liggende igjen pa kameraet. Du trenger ogsa `zbar` for a kunne kjore deler av testene:
```
brew install zbar
brew install gphoto2
```

# Kjøre applikasjon lokalt

Kjør følgende for å starte backend:
```
git clone https://github.com/SimenHolmestad/CameraHub.git
cd CameraHub
python3.13 -m venv .venv
source .venv/bin/activate
pip3 install -r python-requirements.txt
python3 -m scripts.run_backend
```
(neste gang trenger du bare source `.venv/bin/activate && python3 -m scripts.run_backend`)

For å starte frontend, kjør dette i egen terminal.
```
cd CameraHub/frontend
npm install
npm run dev
```

Det er også mulig å kjøre begge deler "i produksjon" lokalt med:
```
source .venv/bin/activate
python3 -m scripts.run_application
```

# Kjøre tester
For å kjøre tester må du ha installert zbar (kan gjøres med `brew install zbar`)
```
export DYLD_LIBRARY_PATH=/opt/homebrew/lib && python3 -m pytest backend/tests
```
