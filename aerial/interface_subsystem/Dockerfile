FROM php:7.4-apache

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y \
    libxml2-dev \
    openssh-server \
    sudo \
 && docker-php-ext-install simplexml \
 && docker-php-ext-install pdo pdo_mysql

COPY html/ /var/www/html/

RUN useradd -m -s /bin/bash kestrel \
 && echo "kestrel:856a0e059c03" | chpasswd

# Configure SSH
RUN mkdir /var/run/sshd \
 && echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config \
 && echo 'PermitRootLogin no' >> /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

COPY ./start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]