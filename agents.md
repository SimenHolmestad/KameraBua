# Agents.md

## Tests
Run backend tests from the .venv:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:/usr/local/lib:$DYLD_LIBRARY_PATH && python3 -m pytest backend/tests
```
