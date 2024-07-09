FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx-or.conf /etc/nginx/nginx.conf
COPY stream.conf /etc/nginx/conf.d/stream

COPY static /usr/share/nginx/html/static/

CMD ["nginx", "-g", "daemon off;"]