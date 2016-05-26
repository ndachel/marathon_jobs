FROM centos
ENV HTTP_PROXY=http://web-proxy.corp.hpecorp.net:8080
ENV HTTPS_PROXY=http://web-proxy.corp.hpecorp.net:8080
ENV NO_PROXY=172.16.1.16,mesos
ENV REFRESH_DELAY=6
ADD yum.conf /etc/yum.conf
RUN yum install -y epel-release
RUN yum update -y
RUN yum install -y haproxy python-pip
RUN mkdir -p /var/lib/haproxy
RUN pip install requests
ADD haproxy.cfg.template /var/lib/haproxy/haproxy.cfg.template
ADD haproxy.last /var/lib/haproxy/haproxy.last
ADD update_cfg.py /var/lib/haproxy/update_cfg.py
ADD run_proxy.sh /var/lib/haproxy/run_proxy.sh
RUN chmod a+x /var/lib/haproxy/run_proxy.sh
CMD /var/lib/haproxy/run_proxy.sh
