import csv
import sys

from sqlalchemy import select

from simplestforms.db import Session
from simplestforms.models import FormSubmission


def main() -> None:
    if len(sys.argv) == 1:
        # no CLI arg, find all columns
        stmt = select(FormSubmission)
        column_set = set()
        with Session() as dbsession:
            with dbsession.begin():
                for submission in dbsession.scalars(stmt):
                    for column in submission.content:
                        column_set.add(column)
        columns = list(column_set)
    else:
        # columns passed as arg, e.g: csv email,first_name,last_name
        columns = sys.argv[1].split(",")
    writer = csv.writer(sys.stdout)
    writer.writerow(
        [
            "created",
            "client_addr",
            *columns,
        ]
    )
    stmt = select(FormSubmission).order_by(FormSubmission.created)
    with Session() as dbsession:
        with dbsession.begin():
            for submission in dbsession.scalars(stmt):
                row_data: list[str] = []
                for column in columns:
                    value = submission.content.get(column, "")
                    if isinstance(value, list):
                        row_data.append(",".join(value))
                    else:
                        row_data.append(value)
                writer.writerow(
                    [
                        submission.created.isoformat(),
                        submission.client_addr,
                        *row_data,
                    ]
                )
