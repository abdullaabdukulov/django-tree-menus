# Base image
FROM postgis/postgis:15-3.3-alpine

# Copy in the postgres-script
COPY postgres-script.sh /docker-entrypoint-initdb.d/
RUN chmod 755 /docker-entrypoint-initdb.d/postgres-script.sh