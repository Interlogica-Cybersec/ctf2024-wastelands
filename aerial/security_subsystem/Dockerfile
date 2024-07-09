FROM php:7.4-apache
WORKDIR /var/www/html
RUN apt-get update && apt-get install -y \
    libxml2-dev \
 && docker-php-ext-install simplexml

RUN docker-php-ext-install pdo pdo_mysql

COPY html/ /var/www/html/
CMD ["apache2-foreground"]
