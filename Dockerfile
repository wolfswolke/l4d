FROM python:3.13.0a6-alpine3.18

RUN apk upgrade && apk add curl
# copying each folder one by one so docker can cache the layers
#COPY . /app
RUN mkdir -p /app/
RUN mkdir -p /app/src
RUN mkdir -p /app/src/logic

WORKDIR /app/src

COPY requirements.txt /app/src/requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

COPY src/start_app.py /app/src/start_app.py
COPY src/flask_definitions.py /app/src/flask_definitions.py

COPY src/config/ /app/src/config/

COPY src/endpoints/ /app/src/endpoints/

COPY src/image/ /app/src/image/
COPY src/static/ /app/src/static/
COPY src/templates/ /app/src/templates/

# Copy logic
COPY src/logic/ /app/src/logic/


EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/api/v1/healthcheck

ENTRYPOINT ["python", "start_app.py"]