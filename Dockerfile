# use slimline python image
FROM python:3.7-alpine

# install project dependencies
COPY requirements.txt /
RUN python3 -m pip install --no-cache -r /requirements.txt
RUN python3 -m pip install --no-cache gunicorn

# configure flask app
WORKDIR /flask_app

COPY online_store ./online_store
COPY manage.py .
COPY products.json .

# run flask app
ENV FLASK_APP_PORT=5000
ENV FLASK_APP=online_store.app:create_app
ENV PYTHONPATH=.
# CMD ["python3", "manage.py", "run"]
CMD ["gunicorn", "${FLASK_APP}()", "-b", "0.0.0.0:$PORT", "-w3"]