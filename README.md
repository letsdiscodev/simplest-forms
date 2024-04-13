# Simplest Forms
Simple service to receive a form from a static HTML site.

## Linters/Formatters

```
bin/ruff check --fix .
bin/ruff format .
bin/mypy .
```

## Generating an Alembic revision

```
docker compose build --no-cache web
docker compose run --rm web rm data/simplestforms.sqlite3
docker compose run --rm web alembic upgrade head
docker compose run --rm web alembic revision --autogenerate -m "0.1.0"
```

## Regenerate requirements.txt

We edit `requirements.in` to list the dependencies.
```bash
docker compose run --rm --no-deps web \
  uv pip compile requirements.in -o requirements.txt
```