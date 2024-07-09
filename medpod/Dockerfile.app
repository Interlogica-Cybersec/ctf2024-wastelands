FROM python:3.11.9-alpine3.19

RUN mkdir /app
COPY static /app/static
COPY templates /app/templates
COPY app.py /app
COPY .env /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "-u", "app.py"]