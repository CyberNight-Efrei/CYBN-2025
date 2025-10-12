# ====== Stage 1: Build ======
FROM php:8.4-cli AS builder

WORKDIR /app
COPY ./src/web /app
COPY ./src/db/db_init.sql /app/db_init.sql

RUN rm -f db.sqlite
RUN php -r ' \
    $dbPath = "db.sqlite"; \
    $db = new PDO("sqlite:$dbPath"); \
    $sql = file_get_contents("db_init.sql"); \
    $db->exec($sql); \
    echo "✅ SQLite DB initialized at $dbPath\n"; \
'


# ====== Stage 2: Runtime ======
FROM php:8.4-fpm

RUN apt-get update && apt-get install -y \
    nginx supervisor sqlite3 libsqlite3-dev \
    && docker-php-ext-install pdo pdo_sqlite \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html
COPY --from=builder /app /var/www/html
COPY ./src/nginx/default.conf /etc/nginx/sites-available/default

RUN mkdir -p /run/php /run/nginx /var/log/supervisor \
    && chown -R www-data:www-data /var/www/html /run/php /run/nginx /var/log

RUN mkdir -p /etc/supervisor/conf.d && \
    echo '[supervisord]\nnodaemon=true\n\n[program:php-fpm]\ncommand=/usr/local/sbin/php-fpm -F\nautostart=true\nautorestart=true\npriority=5\n\n[program:nginx]\ncommand=/usr/sbin/nginx -g "daemon off;"\nautostart=true\nautorestart=true\npriority=10' > /etc/supervisor/conf.d/supervisord.conf

RUN echo '#!/bin/sh\nset -e\ncd /var/www/html\n\nif [ ! -f "db.sqlite" ]; then\n  echo "Initializing SQLite database..."\n  php -r "$db = new PDO(\"sqlite:db.sqlite\"); $sql = file_get_contents(\"db_init.sql\"); $db->exec($sql); echo \"DB initialized.\";"\nfi\n\nexec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf\n' > /entrypoint.sh && chmod +x /entrypoint.sh

ENV FLAG="CYBN{4lw4y5_Ch3ck_ALL_Us3r_D4t4}"

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
