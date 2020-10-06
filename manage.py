import os

from flask.cli import FlaskGroup
from online_store.app import create_app

# TODO: Use a better approach
os.environ['FLASK_APP'] = os.environ.get('FLASK_APP', 'online_shop/app.py')
os.environ['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
os.environ['FLASK_DEBUG'] = "1"

app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
