import logging

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

log.info("Initializing app")

app = FastAPI()

@app.get("/")
def root_get():
    return {"disco": True}

log.info("App initialized")
