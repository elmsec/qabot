# Stage 1 - build frontend app
FROM node:16-alpine as build-deps

WORKDIR /app/

COPY frontend/package.json frontend/package-lock.json /app/
RUN npm install

COPY frontend /app/
RUN npm run generate

# Stage 2 - nginx & frontend dist
FROM nginx:alpine

COPY nginx/prod.conf /etc/nginx/nginx.conf
COPY --from=build-deps /app/.output/public/ /dist/

CMD ["nginx", "-g", "daemon off;"]
