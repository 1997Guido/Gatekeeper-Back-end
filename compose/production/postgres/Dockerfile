FROM postgres:15
# Install PostGIS extension
RUN apt-get update && apt-get install -y postgresql-15-postgis-3
COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
