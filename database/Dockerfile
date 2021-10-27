FROM postgres:13.1
HEALTHCHECK --timeout=45s --interval=5m --retries=10 \
    CMD pg_isready -q -d postgres -U postgres
ENV POSTGRES_PASSWORD="postgres"
ENV PGDATA="/var/lib/postgresql/data/"
ENV PGUSER="postgres"
ENV PGPASSWORD="postgres"
ENV PGDATABASE="postgres"
ENV DB_USER="medical"
ENV DB_PASS="medical"
ENV DB_NAME="medical"
COPY ./init/01-init.sh /docker-entrypoint-initdb.d/
EXPOSE "5432"