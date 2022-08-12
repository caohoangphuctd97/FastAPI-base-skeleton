FROM python:3.8-buster

WORKDIR /workdir
ENV PYTHONPATH "${PYTHONPATH}:/workdir/app"

COPY requirements.txt .
COPY app ./app
RUN pip install -r requirements.txt

COPY .env .
ENV DATABASE_URI='postgresql+psycopg2://postgres:admin@192.168.48.202:5432/saansook'
COPY gunicorn.conf.py .


EXPOSE 8080
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["gunicorn", "--config", "./gunicorn.conf.py", "app.main:app"]