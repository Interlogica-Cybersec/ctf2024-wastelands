FROM python:3.11.9-alpine3.19

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY exposed_git /app/exposed_git
COPY static /app/static
COPY templates /app/templates
COPY .env /app
COPY app.py /app

CMD ["python", "-u", "app.py"]