# frontend/Dockerfile
FROM nginx:alpine

# Удаляем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# Кладём наш конфиг
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Кладём статические файлы
COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css
COPY script.js /usr/share/nginx/html/script.js

EXPOSE 80