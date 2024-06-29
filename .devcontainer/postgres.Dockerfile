FROM postgres:16

RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

RUN apt-get update \
      && apt-get install -y postgresql-contrib \
      && rm -rf /var/lib/apt/lists/*

COPY initdb_citext.sh /docker-entrypoint-initdb.d/citext.sh
