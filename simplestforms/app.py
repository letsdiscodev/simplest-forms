import logging
import uuid
from datetime import datetime, timezone
from typing import Annotated
from urllib.parse import parse_qsl

from fastapi import Depends, FastAPI, Header, HTTPException, Path, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from simplestforms.db import AsyncSession
from simplestforms.models import FormSubmission

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

log.info("Initializing app")


async def get_async_db():
    async with AsyncSession() as dbsession:
        async with dbsession.begin():
            yield dbsession


app = FastAPI()


@app.get("/")
async def root_get():
    return "Simplest Forms"


@app.post("/{form}")
async def root_post(
    dbsession: Annotated[AsyncDBSession, Depends(get_async_db)],
    form: Annotated[str, Path()],
    redirect_to: Annotated[str, Query()],
    x_forwarded_for: Annotated[str, Header()],
    request: Request,
):
    log.info("Saving submission for %s from %s", form, x_forwarded_for)
    body_bytes = await request.body()
    try:
        body_text = body_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=422)
    fields = parse_qsl(body_text)
    content: dict[str, str | list[str]] = {}
    for name, value in fields:
        if name in content:
            old_val = content[name]
            if isinstance(old_val, list):
                new_val = old_val + [value]
            else:
                new_val = [old_val, value]
            content[name] = new_val
        else:
            content[name] = value
    submission = FormSubmission(
        id=uuid.uuid4().hex,
        created=datetime.now(timezone.utc),
        client_addr=x_forwarded_for,
        form=form,
        content=content,
    )
    dbsession.add(submission)
    return RedirectResponse(url=redirect_to, status_code=302)


log.info("App initialized")
