FROM debian:bookworm-slim

MAINTAINER pietro.pizzo@gmail.com

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y apache2 libapache2-mod-php8.1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /usr/share/doc* /usr/share/man/* /usr/share/info/*
RUN a2enmod php8.1 cgi rewrite auth_basic proxy proxy_http

EXPOSE 80

CMD ["apache2ctl", "-D", "FOREGROUND"]
