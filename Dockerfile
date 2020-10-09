# use slimline python image
FROM python:3.7-alpine

# install project dependencies
COPY requirements.txt /
RUN python3 -m pip install --no-cache -r /requirements.txt
COPY manage.py /
COPY online_store/ /flask_app

# run flask app
CMD ["FLASK_APP=flask_app.app:create_app", \
     "python3", "-m", "manage.py", "run"]