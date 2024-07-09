# Use the latest version of Ubuntu as the base image
FROM ubuntu:24.04

# Set environment variables
ENV LANG C.UTF-8
ENV TERM xterm

# Install necessary packages
RUN apt update && \
    apt install -y openssh-server python3 sudo bash && \
    apt clean

# Create users
RUN useradd -m warmachine && \
    echo "warmachine:warmachine" | chpasswd 

# Copy startup.py to the home directory of user warmachine
COPY --chmod=555 startup.py /home/warmachine/startup.py
COPY modules /home/warmachine/modules
COPY --chmod=555 killenemies /usr/local/bin/killenemies

# Set ownership to warmachine user and group
RUN chown -R root:root /home/warmachine
RUN chmod +rx /home/warmachine
RUN chmod 500 /home/warmachine/modules

# Create a file accessible only from root
RUN echo "NTRLGC{Th3_f4st3s7_meCh_in_th3_w4r}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

# Set up user warmachine as sudoer
RUN mkdir -p /etc/sudoers.d/ && \
    echo "warmachine ALL=(ALL) NOPASSWD: /usr/bin/python3 /home/warmachine/startup.py" > /etc/sudoers.d/warmachine

# Generate SSH host keys
RUN ssh-keygen -A

# Create privilege separation directory
RUN mkdir -p /run/sshd

# Expose SSH port
EXPOSE 2222

# Set bash as default shell for user warmachine
RUN chsh -s /bin/bash warmachine

# BANNER 
RUN sed -i '/pam_motd.so/d' /etc/pam.d/sshd
COPY banner /etc/ssh/banner
COPY sshd_config /etc/ssh/sshd_config

# Start SSH service with bash shell
CMD ["/usr/sbin/sshd", "-D", "-e"]
