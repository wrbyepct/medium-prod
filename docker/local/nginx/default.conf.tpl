upstream api {
    server ${API_HOST}:${API_PORT};
}

server {

    listen ${LISTEN_PORT};

    location /staticfiles {
        alias /vol/api/staticfiles;
    }

    location /mediafiles {
        alias /vol/api/mediafiles;
    }

    location / {

        proxy_pass  http://api;
        include     /etc/nginx/proxy_params;
        client_max_body_size 20M;

    }


}
