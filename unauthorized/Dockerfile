FROM python:3.9-slim

COPY server.py server.py
COPY logo.png logo.png
COPY logo2.png logo2.png
COPY glitch.ico glitch.ico
COPY glitch.html glitch.html
ENV PYTHONUNBUFFERED=1

CMD ["python", "-BOu", "server.py"]
