[Tilbake til readme](../readme.md)

# Generer frontend API-typer

Frontend-klienten og typene genereres fra backendens OpenAPI-skjema.

Kjør dette fra repo-roten:
```
python3 -m scripts.generate_frontend_types
```

Scriptet starter backend, venter på `/openapi.json`, genererer klienten til `frontend/src/api`, og stopper backenden igjen.
