FROM postgres:15-bullseye

# copy maintenence files to container 

COPY ./maintenance/ /usr/local/bin/maintenance

RUN chmod +x /usr/local/bin/maintenance/*

RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
