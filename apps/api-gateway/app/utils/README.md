# Utility Module (`app/utils/`)

## Purpose
The `app/utils/` module provides pure side-effect-free helper functions, string validators, timezone-aware datetime parsers, and pagination response builders.

## Responsibilities
- **`datetime.py`**: Timezone-aware UTC timestamp generators (`utc_now()`).
- **`helpers.py`**: String formatting and UUID v4 generators.
- **`validators.py`**: Regex format validators.
- **`pagination.py`**: Standard pagination dictionary wrapper constructors.

## What Belongs Here
- Pure utility functions with zero side-effects.

## What Should NOT Belong Here
- FastAPI endpoint handlers, DB queries, or stateful service logic.
