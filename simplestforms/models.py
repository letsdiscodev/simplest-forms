from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import MetaData
from sqlalchemy.types import JSON

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: https://alembic.sqlalchemy.org/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

base_metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(AsyncAttrs, DeclarativeBase):
    metadata = base_metadata
    type_annotation_map = {dict[str, Any]: JSON}


class FormSubmission(Base):
    __tablename__ = "form_submissions"
    id: Mapped[str] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(index=True)
    client_addr: Mapped[str] = mapped_column(index=True)
    form: Mapped[str] = mapped_column(index=True)
    content: Mapped[dict[str, Any]]

    def __repr__(self) -> str:
        return f"FormSubmission(id={self.id!r})"
