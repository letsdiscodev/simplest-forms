import csv
import sys
from dataclasses import dataclass

from sqlalchemy import select

from simplestforms.db import Session
from simplestforms.models import FormSubmission


@dataclass
class CLIArgs:
    columns: list[str] | None
    form: str | None


def parse_cli_args() -> CLIArgs:
    columns: str | None = None
    form: str | None = None
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if len(args) <= i + 1:
            # args are in pair (--name value)
            # we reached the last arg,
            # no need to check for --name
            continue
        if arg == "--columns" and len(args) > i + 1:
            columns = args[i + 1]
        elif arg == "--form":
            form = args[i + 1]
    return CLIArgs(
        columns=columns.split(",") if columns is not None else None, form=form
    )


def main() -> None:
    args = parse_cli_args()
    if args.columns is None:
        # no CLI arg, find all columns
        stmt = select(FormSubmission)
        if args.form is not None:
            stmt = stmt.where(FormSubmission.form == args.form)
        column_set = set()
        with Session() as dbsession:
            with dbsession.begin():
                for submission in dbsession.scalars(stmt):
                    for column in submission.content:
                        column_set.add(column)
        columns = list(column_set)
    else:
        columns = args.columns
    writer = csv.writer(sys.stdout)
    writer.writerow(
        [
            "created",
            "client_addr",
            "form",
            *columns,
        ]
    )
    stmt = select(FormSubmission)
    if args.form is not None:
        stmt = stmt.where(FormSubmission.form == args.form)
    stmt = stmt.order_by(FormSubmission.created)
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
                        submission.form,
                        *row_data,
                    ]
                )
