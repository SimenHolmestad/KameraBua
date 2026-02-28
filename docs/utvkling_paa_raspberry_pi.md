[Tilbake til readme](../readme.md)

# Utvikling på Raspberry PI (for rask feedback-loop)
En del kamerating er ikke så greit å teste lokalt, så da er det fint å få til en rask feedback-loop.

Først, logg inn med SSH i et terminalvindu og sett opp ting riktig:

```
ssh <brukernavn>@<ip-adresse>
cd ~/CameraHub
source .venv/bin/activate
```
bytt til branchen du jobber på med
```
git checkout <branch_name>
```

Du kan nå kjøre følgende for å teste det du har commitet opp:

```
git pull && sudo .venv/bin/python -m scripts.update_and_redeploy --env-file ./.env
```

Hvis du vet at du kun skal gjøre backend-endringer går det mye fortere å gjøre:
```
git pull && sudo .venv/bin/python -m scripts.update_and_redeploy --env-file ./.env --skip-frontend-build
```

Med `git commit --amend` går dette ganske fort.
