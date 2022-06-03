# Build Stage 1
FROM node:16-alpine3.14 AS build-stage
RUN mkdir /app
WORKDIR /app
COPY ./reactapp .
RUN npm install
RUN npm run build
# Build Stage 2
FROM nginx
WORKDIR /app
COPY --from=build-stage /app/build/ /usr/share/nginx/html
COPY ./default.conf /etc/nginx/conf.d/default.conf 
CMD ["nginx", "-g", "daemon off;"]