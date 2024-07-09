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
RUN useradd -m mechcore && \
    echo "mechcore:mechcore" | chpasswd 

# Copy startup.py to the home directory of user mechcore
COPY --chmod=555 startup.py /home/mechcore/startup.py
COPY modules /home/mechcore/modules

# Set ownership to mechcore user and group
RUN chown -R root:root /home/mechcore
RUN chmod +rx /home/mechcore
RUN chmod 500 /home/mechcore/modules

# Create a file accessible only from root
RUN echo "NTRLGC{The_f4st3r_mecH_1n_c0mb4t}" > /root/flag.txt && \
    chmod 600 /root/flag.txt

# Set up user mechcore as sudoer
RUN mkdir -p /etc/sudoers.d/ && \
    echo "mechcore ALL=(ALL) NOPASSWD: /usr/bin/python3 /home/mechcore/startup.py" > /etc/sudoers.d/mechcore

# Generate SSH host keys
RUN ssh-keygen -A

# Create privilege separation directory
RUN mkdir -p /run/sshd

# Expose SSH port
EXPOSE 2222

# Set bash as default shell for user mechcore
RUN chsh -s /bin/bash mechcore

# BANNER 
RUN sed -i '/pam_motd.so/d' /etc/pam.d/sshd
COPY banner /etc/ssh/banner
COPY sshd_config /etc/ssh/sshd_config

# GLITCH
COPY --chmod=644 glitch.txt /home/mechcore/glitch.txt


# Start SSH service with bash shell
CMD ["/usr/sbin/sshd", "-D", "-e"]
