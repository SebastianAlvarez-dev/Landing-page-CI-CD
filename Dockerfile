# Usamos un servidor ligero de Nginx para servir archivos estáticos
FROM nginx:alpine
# Copiamos tus archivos a la carpeta donde Nginx los muestra
COPY . /usr/share/nginx/html
# Exponemos el puerto 80
EXPOSE 80