# pastebin

This is a simple utility application where we can paste; put files, text, etc.
Then bin which is easily extract the files, images, movies, etc. at will.

## Development Environment

Install [uv](https://docs.astral.sh/uv/)

```zsh
brew install uv
```

Initialize Project

```zsh
uv init pastebin
cd pastebin
```

Setup **venv**

```zsh
uv venv
source .venv/bin/activate
```

Install Dependencies

```zsh
uv add fastapi uvicorn[standard] jinja2 python-multipart
```

Install Options

```zsh
uv add pydantic-settings
uv add sqlalchemy alembic asyncpg  # if Postgres
uv add httpx                       # external API calls
uv add rich                        # nicer logs locally
```

Developer Testing Options

```zsh
uv add --dev pytest pytest-asyncio ruff mypy
```

Run the App

```zsh
uv run uvicorn app.main:app --reload
```

### Folder Structure

```zsh
myapp/
  pyproject.toml
  uv.lock
  README.md

  app/
    main.py                 # app factory / FastAPI instance
    config.py               # settings (env-driven)
    logging.py              # optional
    dependencies.py         # shared deps (db session, auth, etc.)

    api/                    # JSON API routes (if you have them)
      __init__.py
      v1/
        __init__.py
        routes/
          health.py
          users.py

    web/                    # HTML page routes (templates)
      __init__.py
      routes/
        home.py
        auth.py

    templates/              # Jinja2 templates
      base.html
      home/
        index.html
      auth/
        login.html

    static/                 # served static assets
      css/
      js/
      img/

    domain/                 # pure business logic (no FastAPI imports)
      __init__.py
      users/
        models.py
        service.py

    infra/                  # integrations (db, email, external APIs)
      __init__.py
      db/
        session.py
        models.py
        repository.py

  tests/
    test_health.py
    web/
      test_home.py

  scripts/
    dev.sh

```
