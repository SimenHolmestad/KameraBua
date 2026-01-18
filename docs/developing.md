[Back to readme](../README.md)

# Developing
Under utvikling vil applikasjonen lage bilder som dette når det ikke er noe kamera koblet til:

![Dummy demo circle image](images/dummy_demo_image.png)

Kjør følgende for å starte backend:
```
git clone https://github.com/SimenHolmestad/CameraHub.git
cd CameraHub
python3.13 -m venv .venv
source .venv/bin/activate
pip3 install -r python-requirements.txt
export FLASK_ENV=development
python3 -m scripts.run_application
```
For å kjøre kun backend uten å bygge frontend, bruk:
```
python3 -m scripts.run_backend
```

For å starte frontend, kjør dette i egen terminal.
```
cd CameraHub/frontend
npm install
npm start
```

# Kjøre tester
```
python3 -m unittest
```
