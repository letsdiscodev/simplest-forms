FROM python:3.12.2
ENV PYTHONUNBUFFERED 0
RUN apt-get update
RUN pip install uv
WORKDIR /app
COPY pyproject.toml /app/
COPY requirements.txt /app/
ADD alembic.ini /app/alembic.ini
RUN pip install -r requirements.txt
ADD simplestforms /app/simplestforms
RUN pip install -e .
CMD ["uvicorn", "simplestforms.app:app", "--port", "8000", "--host", "0.0.0.0"]