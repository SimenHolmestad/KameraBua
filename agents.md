# Agents.md

## Tests
Run backend tests from the .venv:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib && python3 -m pytest backend/tests
```

Make sure to run the tests after doing larger changes. Do not ask to run the tests, just do it.

## Frontend Types
When changes affect both the backend and frontend API surface, run the type generation script:

```sh
python3 -m scripts.generate_frontend_types
```
