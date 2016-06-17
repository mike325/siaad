FROM python:3.4-slim
MAINTAINER Mike "docker@prodeveloper.me"

RUN apt-get update && apt-get install -y \
    gcc \
    gettext \
    mysql-client libmysqlclient-dev \
    postgresql-client libpq-dev \
    sqlite3 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV DJANGO_VERSION 1.9.7

RUN pip install mysqlclient psycopg2 django=="$DJANGO_VERSION"

RUN apt-get install apache2 apache2-mpm-prefork apache2-utils libexpat1 ssl-cert -y
RUN apt-get install libapache2-mod-wsgi -y

WORKDIR /tmp

RUN rm /etc/apache2/apache2.conf
ADD apache2.conf /etc/apache2/apache2.conf

ADD clean_install /tmp/SistemaAdministratrivo

RUN mkdir -p /var/www/SistemaAdministratrivo/ && \
    cp -R /tmp/SistemaAdministratrivo /var/www/SistemaAdministratrivo/

RUN cd SistemaAdministratrivo/ && \
    pip install -r requirements.txt

#RUN service apache2 start

WORKDIR /tmp
ADD start.sh /tmp/start.sh
RUN chmod 0755 /tmp/start.sh

EXPOSE 80

CMD ["bash", "start.sh" ]
