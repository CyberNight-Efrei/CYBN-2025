# ====== Stage 1: Build dependencies ======
FROM composer:2 AS builder

WORKDIR /app
COPY ./src/web /app

# ===== Default environment =====
ENV APP_ENV=prod
ENV DATABASE_URL="sqlite:///%kernel.project_dir%/var/data.db"
ENV FLAG="CYBN{0RM_C4NT_F1X_B4D_D3VS}"

# Install everything (including dev) to allow cache warmup
RUN composer install --no-interaction --no-progress --optimize-autoloader \
    && php bin/console cache:clear --env=prod --no-warmup \
    && php bin/console cache:warmup --env=prod \
    && rm -rf var && mkdir var && touch var/data.db \
    && php bin/console doctrine:migrations:migrate --no-interaction --env=prod \
    && php bin/console doctrine:fixtures:load --no-interaction \
    && composer install --no-dev --no-interaction --no-progress --optimize-autoloader


# ====== Stage 2: Runtime ======
FROM php:8.4-fpm

RUN apt-get update && apt-get install -y \
    nginx supervisor unzip git libicu-dev libzip-dev zip sqlite3 libsqlite3-dev \
    && docker-php-ext-install intl pdo pdo_sqlite opcache zip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html
COPY --from=builder /app /var/www/html

RUN mkdir -p var/log var/cache /run/php /run/nginx /var/log/supervisor \
    && chown -R www-data:www-data var /run/php /run/nginx /var/log /var/log/supervisor

COPY ./src/nginx/default.conf /etc/nginx/sites-available/default

RUN mkdir -p /etc/supervisor/conf.d && \
    echo '[supervisord]\nnodaemon=true\n\n[program:php-fpm]\ncommand=/usr/local/sbin/php-fpm -F\nautostart=true\nautorestart=true\npriority=5\n\n[program:nginx]\ncommand=/usr/sbin/nginx -g "daemon off;"\nautostart=true\nautorestart=true\npriority=10' > /etc/supervisor/conf.d/supervisord.conf

RUN echo '#!/bin/sh\nset -e\n\ncd /var/www/html\n\nrm -rf var\nmkdir -p var\ntouch var/data.db\n\nif [ -f "bin/console" ]; then\n  php bin/console cache:clear --env=prod --no-warmup || true\n  php bin/console cache:warmup --env=prod || true\n  php bin/console doctrine:migrations:migrate --no-interaction --env=prod || true\n  php bin/console doctrine:fixtures:load --no-interaction || true\nfi\n\nexec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf\n' > /entrypoint.sh

RUN chmod +x /entrypoint.sh

# ===== Default environment =====
ENV APP_ENV=prod
ENV DATABASE_URL="sqlite:///%kernel.project_dir%/var/data.db"
ENV FLAG="CYBN{0RM_C4NT_F1X_B4D_D3VS}"

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
