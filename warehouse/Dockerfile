FROM python:3.11.9-alpine3.19

RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY static /app/static
COPY templates /app/templates
COPY commands /app/commands
COPY app.py /app
COPY .env /app
WORKDIR /app

CMD ["python", "-u", "app.py"]