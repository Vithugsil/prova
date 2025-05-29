FROM php:8.1-cli

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y \
    git zip unzip \
    libssl-dev libcurl4-openssl-dev \
    && docker-php-ext-install sockets

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

COPY . .

RUN composer install

EXPOSE 80
CMD ["php", "-S", "0.0.0.0:80", "index.php"]
