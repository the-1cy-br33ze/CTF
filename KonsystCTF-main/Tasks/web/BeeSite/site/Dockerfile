# Используем легковесный nginx
FROM nginx:alpine

# Копируем файлы сайта
COPY site/ /usr/share/nginx/html

# Копируем конфиг nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80
EXPOSE 80

# Запускаем ngi

CMD ["nginx", "-g", "daemon off;"]