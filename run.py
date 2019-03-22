import click
from app import app, db, Supporter


@app.cli.command()
def bootstrap():
    db.create_all()
    db.session.commit()
