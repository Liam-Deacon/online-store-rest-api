# use slimline python image
FROM python:3.7-alpine

# install project dependencies
COPY requirements.txt /
RUN python3 -m pip install --no-cache -r /requirements.txt
COPY online_store /flask_app/
COPY manage.py /flask_app/

# run flask app
WORKDIR /flask_app
ENV FLASK_APP=online_store.app:create_app
CMD ["python3", "-m", "manage.py", "run"]