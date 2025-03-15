FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./proxy_params /etc/nginx/proxy_params
COPY ./entrypoint /entrypoint

USER root

RUN mkdir -p /vol/api \
    && chmod 755 /vol/api \
    && touch /etc/nginx/conf.d/default.conf \
    && chown nginx:nginx /etc/nginx/conf.d/default.conf \
    && sed -i "s/\r$//g" /entrypoint \
    && chmod +x /entrypoint

USER nginx

ENTRYPOINT ["/entrypoint"]