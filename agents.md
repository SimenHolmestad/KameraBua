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
## Backwards compatibility
There is never a need to make the api (or any other code) backwards compatible. The frontend and backend ships together.

## Plans
- Make the plan extremely concise. Sacrifice grammar for the sake of concision.
- At the end of each plan, give me a list of unresolved questions to answer, if any.
