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
RUN useradd -m wartank && \
    echo "wartank:wartank" | chpasswd 

# Copy startup.py to the home directory of user wartank
COPY --chmod=555 startup.py /home/wartank/startup.py
COPY modules /home/wartank/modules
COPY --chmod=555 killenemies /usr/local/bin/killenemies

# Set ownership to wartank user and group
RUN chown -R root:root /home/wartank
RUN chmod +rx /home/wartank
RUN chmod 500 /home/wartank/modules

# Create a file accessible only from root
RUN echo "NTRLGC{Collide_w1th_This_t4nK}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

# Set up user wartank as sudoer
RUN mkdir -p /etc/sudoers.d/ && \
    echo "wartank ALL=(ALL) NOPASSWD: /usr/bin/python3 /home/wartank/startup.py *" > /etc/sudoers.d/wartank

# Generate SSH host keys
RUN ssh-keygen -A

# Create privilege separation directory
RUN mkdir -p /run/sshd

# Expose SSH port
EXPOSE 2222

# Set bash as default shell for user wartank
RUN chsh -s /bin/bash wartank

# BANNER 
RUN sed -i '/pam_motd.so/d' /etc/pam.d/sshd
COPY banner /etc/ssh/banner
COPY sshd_config /etc/ssh/sshd_config

# Start SSH service with bash shell
CMD ["/usr/sbin/sshd", "-D", "-e"]
