# Fetching the latest nginx image
FROM nginx:latest

# Removing default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Copying our nginx.conf
COPY nginx.conf /etc/nginx/conf.d

# CMD ["/run.sh"]