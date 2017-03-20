FROM richarvey/nginx-php-fpm
#ENV http_proxy=http://web-proxy.corp.hpecorp.net:8080
#ENV https_proxy=http://web-proxy.corp.hpecorp.net:8080
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9D6D8F6BC857C906
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7638D0442B90D010
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7638D0442B90D010
#RUN apt-get update 
#RUN sh -c '/bin/echo -e "Y" | apt-get install -y nginx'
#RUN apt-get install -y php7.0-common php7.0-cli php7.0-fpm

ADD ./files /var/www/html
#ADD ./files/nginx.conf /etc/nginx/nginx.conf
#ADD ./files/sites-available-default /etc/nginx/sites-available/default

EXPOSE 80
#CMD sed -e "s/CONTAINERID/'$(hostname)'/g" /usr/share/nginx/html/index.html > /usr/share/nginx/html/index.html.tmp && mv /usr/share/nginx/html/index.html.tmp /usr/share/nginx/html/index.html && nginx -g "daemon off;"
