FROM nginx:latest
LABEL maintainer="github.com/ojg1993"

COPY ./default.conf /etc/nginx/conf.d/default.conf

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx