# Stage 1: Node image to build React project
FROM node:latest as build-stage

WORKDIR /app

# Clone your React project
RUN git clone https://github.com/1997Guido/Gatekeeper-Front-end.git .
WORKDIR /app/gatekeeper
# Install dependencies and build the project
RUN yarn install
RUN yarn build

# Stage 2: Set up Nginx to serve the React app
FROM nginx:1.17.8-alpine

# Copy the Nginx configuration file
COPY ./compose/production/nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy the built React app from the build stage
COPY --from=build-stage /app/gatekeeper/build /usr/share/nginx/html

# Create directories for Django's static and media files
# and set appropriate permissions
RUN mkdir -p /usr/share/nginx/media \
    && chown -R nginx:nginx /usr/share/nginx/media \
    && mkdir -p /usr/share/nginx/static \
    && chown -R nginx:nginx /usr/share/nginx/static

# The default.conf should be configured to serve /media/ and /static/
