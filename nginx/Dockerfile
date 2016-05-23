FROM nelsd/nginx-blue
ADD ./index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD sed -e "s/CONTAINERID/'$(hostname)'/g" /usr/share/nginx/html/index.html > /usr/share/nginx/html/index.html.tmp && mv /usr/share/nginx/html/index.html.tmp /usr/share/nginx/html/index.html && nginx -g "daemon off;"
