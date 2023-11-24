FROM nginx:1.17.8-alpine

# Copy the Nginx configuration file
COPY ./compose/production/nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy the React app's build directory to the container
# Adjust the source path according to your project structure
COPY ./compose/production/nginx/react/build /usr/share/nginx/html

# Create directories for Django's static and media files
# and set appropriate permissions
RUN mkdir -p /usr/share/nginx/media \
    && chown -R nginx:nginx /usr/share/nginx/media \
    && mkdir -p /usr/share/nginx/static \
    && chown -R nginx:nginx /usr/share/nginx/static

# Ensure that the default.conf file is configured to serve
# /media/ and /static/ using the directories created above.