FROM ubuntu:16.04
ENV http_proxy=http://web-proxy.corp.hpecorp.net:8080
ENV https_proxy=http://web-proxy.corp.hpecorp.net:8080
ENV no_proxy=172.16.1.16,mesos
RUN apt-get update && \
    apt-get install -y wget
RUN apt-get install -y openjdk-8-jre
RUN wget https://download.elasticsearch.org/logstash/logstash/packages/debian/logstash_1.4.2-1-2c0f5a1_all.deb -O /tmp/logstash.deb 
RUN wget https://download.elasticsearch.org/logstash/logstash/packages/debian/logstash-contrib_1.4.2-1-efd53ef_all.deb -O /tmp/logstash-contrib.deb 
RUN dpkg -i /tmp/logstash.deb
RUN dpkg -i /tmp/logstash-contrib.deb 
RUN apt-get -f -y install
RUN rm -rf /tmp/logstash.deb /tmp/logstash-contrib.deb
COPY logstash.conf /etc/logstash.conf
EXPOSE 5000
CMD [/opt/logstash/bin/logstash -f /etc/logstash.conf]
