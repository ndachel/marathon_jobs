# marathon_jobs
This repo contains severl separate marathon jobs for testing the DCOS cluster.
Maybe the most interesting job is the haproxy job.
  --It includes a Dockerfile that builds a container that watches the Marathon tasks API and then checks for services 
  that are marked for balancing in etcd (running somewhere else).
  --It then rebuilds the haproxy.cfg and restarts the haproxy service when needed. 
  --This allows for you to proxy all instances of an internal service on an external port. 
  --In production you would want to constrain this service to a public slave
