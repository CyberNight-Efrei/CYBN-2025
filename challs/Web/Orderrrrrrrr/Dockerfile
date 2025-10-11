FROM php:8.4-fpm

# Install system dependencies and PHP extensions
RUN apt-get update && apt-get install -y \
    unzip git libicu-dev libzip-dev zip sqlite3 libsqlite3-dev \
    && docker-php-ext-install intl pdo pdo_sqlite opcache zip \
    && rm -rf /var/lib/apt/lists/*

# Copy Composer binary
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

# Copy only composer files first (better layer caching and ensures install works)
COPY ./src/web/composer.json ./src/web/composer.lock* ./

# Install PHP dependencies
RUN composer install --no-dev --no-scripts --no-interaction --optimize-autoloader

# Copy the rest of the app after installing dependencies
COPY ./src/web /var/www/html

# Prepare app directories and warm Symfony cache
RUN mkdir -p var \
    && chown -R www-data:www-data var \
    && php bin/console cache:clear --env=prod --no-warmup \
    && php bin/console cache:warmup --env=prod
