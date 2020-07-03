from click import command, echo
from flask.cli import with_appcontext

from backend import create_app, db


@command("init-db")
@with_appcontext
def init_database():
    db.create_all()
    echo("Initialization of database.")


app = create_app()
app.cli.add_command(init_database)
