FROM php:8.4-fpm

RUN apt-get update && apt-get install -y \
    unzip git libicu-dev libzip-dev zip sqlite3 libsqlite3-dev \
    && docker-php-ext-install intl pdo pdo_sqlite opcache zip \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

COPY ./src/web /var/www/html

RUN rm -rf var/cache/* var/log/* \
    && composer install --no-dev --no-scripts --no-interaction --optimize-autoloader \
    && php bin/console cache:clear --env=prod --no-warmup \
    && php bin/console cache:warmup --env=prod \
