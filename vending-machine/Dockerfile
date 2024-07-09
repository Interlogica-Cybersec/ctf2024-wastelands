FROM ubuntu:24.04

# Installa OpenSSH Server
RUN apt-get update && apt-get install -y openssh-server vim sudo python3-pip python3-colorama && \
    mkdir /var/run/sshd

# Avvia SSH
CMD ["/usr/sbin/sshd", "-D"]

# Crea l'utente guest:guest con /home/guest
RUN useradd -m -d /home/guest -s /bin/bash -p $(echo guest | openssl passwd -1 -stdin) guest

# Copia lo script CLI.py nella home
COPY CLI.py /home/guest/CLI.py

# Imposta la shell di guest su CLI.py
RUN chsh -s /home/guest/CLI.py guest

# Aggiungi l'utente guest ai sudoers
RUN echo "guest ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Setta permessi a CLI.py
RUN chown root:root /home/guest/CLI.py && \
    chown root:root /home/guest && \
    chmod 755 /home/guest && \
    chmod +x /home/guest/CLI.py
	
# Crea log
RUN mkdir -p /home/guest/log && \
    touch /home/guest/log/last24h.log /home/guest/log/auth.log /home/guest/log/err.log && \
	chown guest:guest /home/guest/log
	
# Genera flag
RUN echo "NTRLGC{V3ND1NG+M4CH1N35+T0MB+R41D3R}" > /home/guest/door_opening_code && \
	chmod 700 /home/guest/door_opening_code

# Copia motd e issue
COPY motd /etc/

# Fixa un po di merda
RUN echo "Banner /etc/motd" >> /etc/ssh/sshd_config && \
	echo "PrintMotd no"

# Togli banner ubuntu
RUN sed -i '/^session[[:space:]]\+optional[[:space:]]\+pam_motd\.so[[:space:]]\+motd=\/run\/motd\.dynamic$/s/^/#/' /etc/pam.d/sshd
RUN sed -i '/^session[[:space:]]\+optional[[:space:]]\+pam_motd\.so[[:space:]]\+noupdate$/s/^/#/' /etc/pam.d/sshd

# Magie
RUN rm /bin/chmod && \
	rm /bin/chsh && \
	rm /bin/chown && \
	rm /bin/mount