FROM registry.gitlab.com/zonarsystems/consolidation-layer/data-platform-base-containers/fastapi-base:latest

ARG SSH_PRIVATE_KEY_B64

WORKDIR /workdir
ENV PYTHONPATH "${PYTHONPATH}:/workdir/app"

COPY requirements.txt .

RUN install-python-packages -r requirements.txt

COPY alembic.ini .
COPY gunicorn.conf.py .
COPY migrations ./migrations
COPY app ./app

EXPOSE 8080
CMD ["ddtrace-run", "gunicorn", "--config", "./gunicorn.conf.py", "app.main:app"]