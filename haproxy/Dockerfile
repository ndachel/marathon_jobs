FROM haproxy:latest
RUN mkdir -p /var/lib/haproxy
RUN useradd haproxy
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
