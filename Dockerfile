FROM nginx:1.27-alpine
RUN apk add --no-cache curl jq
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY assets/ /usr/share/nginx/html/assets/
COPY docker/ig-sync.sh /usr/local/bin/ig-sync.sh
COPY docker/40-ig-cron.sh /docker-entrypoint.d/40-ig-cron.sh
RUN chmod +x /usr/local/bin/ig-sync.sh /docker-entrypoint.d/40-ig-cron.sh
VOLUME /data
EXPOSE 80
