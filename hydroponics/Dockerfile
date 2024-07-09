FROM php:8.2-apache

RUN a2enmod proxy
RUN a2enmod proxy_http
RUN echo "ProxyRequests On" >> /etc/apache2/apache2.conf


RUN apt update
RUN apt -y install vsftpd
RUN addgroup --gid 995 --system ftp_user
RUN adduser --gid 995 --home /home/ftp_user --shell /bin/false --uid 995 ftp_user --gecos "" --disabled-password
RUN mkdir -p /home/ftp_user
RUN chown -R ftp_user:ftp_user /home/ftp_user

# hardcoded. yes. >:o
RUN echo "ftp_user:fwjGF12oj3r928jrn123" >> /usr/sbin/chpasswd
COPY docker/vsftpd.conf /etc/vsftpd.conf
RUN cat /etc/vsftpd.conf | sed 's/\r$//' > /etc/vsftpd2.conf; rm /etc/vsftpd.conf; mv /etc/vsftpd2.conf /etc/vsftpd.conf
RUN mkdir -p /data/public
ARG PASSCODE
ENV PASSCODE $PASSCODE
RUN echo '{"active":true,"command":"./plzrun.sh"}' > /data/public/$PASSCODE
RUN chown -R nobody:nogroup /data/public

COPY docker/start.sh /start.sh
RUN cat /start.sh | sed 's/\r$//' > /start2.sh & rm /start.sh & mv /start2.sh /start.sh
RUN chmod +x /start.sh

COPY static /var/www/html/static
COPY php /var/www/html/
WORKDIR /var/www/html/

CMD ["/start.sh"]