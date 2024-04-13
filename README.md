# Simplest Forms
Simple service to receive a form from a static HTML site.

## Deployment

To deploy on Disco the first time:

```bash
disco projects:add \
  --name forms \
  --domain forms.example.com \
  --github-repo https://github.com/letsdiscodev/simplest-forms \
  --deploy 
```

To update to the latest version:
```bash
disco deploy --project forms
```

## Submitting values

Example
```html
<form
  method="POST"
  action="https://forms.example.com/launch-list?redirect_url=https://example.com/launch-page/subscribed"
>
  <p>
    <label for="email">Email</label>
    <input type="email" name="email"/>
  </p>
  <p>
    <label for="first_name">First Name</label>
    <input type="text" name="first_name"/>
  </p>
  <p><button type="submit">Submit</button></p>
</form>
```

This will submit the values for the form `launch-list`, with the fields `email` and `first_name`.


## Exporting values

### Save to a CSV file

```bash
disco run --project forms "csv" > ~/submissions.csv
```
### Output CSV in terminal

```bash
disco run --project forms "csv"
```

### Specify columns

To filter, or simply to re-order.

```bash
disco run --project forms "csv --columns email,first_name"
```

### Specify form

```bash
disco run --project forms "csv --form launch-list"
```

### Specify both columns and form

```bash
disco run --project forms "csv --columns email,first_name --form launch-list"
```

## Development

### Linters/Formatters

```bash
bin/ruff check --fix .
bin/ruff format .
bin/mypy .
```

### Generating an Alembic revision

```bash
docker compose build --no-cache web
docker compose run --rm web rm data/simplestforms.sqlite3
docker compose run --rm web alembic upgrade head
docker compose run --rm web alembic revision --autogenerate -m "0.1.0"
```

### Regenerate requirements.txt

We edit `requirements.in` to list the dependencies.
```bash
docker compose run --rm --no-deps web \
  uv pip compile requirements.in -o requirements.txt
```