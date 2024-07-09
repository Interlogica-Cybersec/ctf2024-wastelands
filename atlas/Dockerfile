# Usa un'immagine base di Ubuntu
FROM ubuntu:24.04

# Evita prompt interattivi durante la costruzione dell'immagine
ARG DEBIAN_FRONTEND=noninteractive

# Installa Python e altri strumenti necessari
RUN apt-get update && \
    apt-get install -y python3 python3-pip sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Crea l'utente 'com'
RUN useradd -m -s /bin/bash com
RUN echo 'com:com123' | chpasswd


# Copy network.py 
COPY network.py /opt/network.py

# Crea la directory /data
RUN mkdir /data

# Copia sensor.py nella root directory e rendilo eseguibile
COPY sensor.py /root/sensor.py
RUN chmod +x /root/sensor.py

# Copia link.py in /opt/ e imposta i permessi e la proprietà corretti
COPY link.py /opt/link.py
RUN chown com:com /opt/link.py &&\
	chmod 710 /opt/link.py
	
# Copia core in /root
COPY core /root/
RUN chmod 700 /root/core
	
COPY broadcast /usr/local/bin
COPY telemetry /usr/local/bin

RUN chmod +x /usr/local/bin/broadcast \
    && chmod +x /usr/local/bin/telemetry

COPY sudoers /etc/
RUN	chmod 640 /etc/sudoers

# Esegui gli script all'avvio: sensor.py come root e link.py come utente 'com'
CMD /root/sensor.py & su com -c '/opt/link.py'
