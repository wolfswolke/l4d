FROM python:3.13.0a6-alpine3.18

LABEL authors="ZKWolf"
ENV TZ="Europe/Vienna" \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app/src

RUN apk upgrade && apk add --no-cache curl

COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del .build-deps

COPY src/ .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/api/v1/healthcheck || exit 1

ENTRYPOINT ["python", "start_app.py"]