# Start from the base image
FROM y1nglamore/cve_2022_44268:latest

RUN apt update
RUN apt-get install -y --no-install-recommends \
    unzip \
    apache2 \
    php \
    libapache2-mod-php 

# Create flag
RUN useradd -m jacobb
RUN echo "NTRLGC{sh4r1ng_0d4yz_t0_fr13ndz_is_4lw4ys_FUN}" > /home/jacobb/key

COPY survivorshub/ /var/www/html/sharing/

RUN chown -R www-data:www-data /var/www/html/sharing && \
    chmod -R 700 /var/www/html/sharing

# Create directory for modified files
RUN mkdir -p /var/www/html/sharing/resized && \
    chown -R www-data:www-data /var/www/html/sharing/uploads && \
    chown -R www-data:www-data /var/www/html/sharing/resized && \
    chmod 700 /var/www/html/sharing/resized && \
    chmod 700 /var/www/html/sharing/uploads

# Fix apache configs
COPY apache2.conf /etc/apache2/apache2.conf
COPY 000-default.conf /etc/apache2/sites-enabled/000-default.conf

# Start Apache service
CMD ["apachectl", "-D", "FOREGROUND"]

