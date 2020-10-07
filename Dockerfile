# use slimline python image
FROM python:3.7-alpine

# install project dependencies
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY online_store/ /app

# run flask app
WORKDIR /app
ENV FLASK_DEBUG=1
CMD ["flask", "run"]