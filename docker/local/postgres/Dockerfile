FROM postgres:15-bullseye

# copy maintenence files to container 

COPY ./docker/local/postgres/maintenence/ /usr/local/bin/maintenence

RUN chmod +x /usr/local/bin/maintenence/*

RUN mv /usr/local/bin/maintenence/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenence