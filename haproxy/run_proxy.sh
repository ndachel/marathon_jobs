#!/bin/bash
printf "\n#############################################################"
printf "\n## `date`: Starting ha proxy watcher ##"
printf "\n#############################################################"
while true;
do
  # copy config to last
  if [ -f /var/lib/haproxy/haproxy.cfg ]
  then
    cp /var/lib/haproxy/haproxy.cfg /var/lib/haproxy/haproxy.last
  fi
    
  # Update proxy config
  python /var/lib/haproxy/update_cfg.py

  # Compare
  DIFF=$(diff /var/lib/haproxy/haproxy.cfg /var/lib/haproxy/haproxy.last) 
  if [ "$DIFF" != "" ] 
  then
    printf "\n`date`: Detected config change"
    if [ -f /var/lib/haproxy/ha-pid ]
      then
      printf "\n`date`: Killing haproxy... PID: `cat /var/lib/haproxy/ha-pid`"
      kill $(cat /var/lib/haproxy/ha-pid)
    fi 
    printf "\n`date`: Restarting haproxy"
    haproxy -f /var/lib/haproxy/haproxy.cfg -p /var/lib/haproxy/ha-pid
  fi
  # sleep for a while
  # for ((q=$REFRESH_DELAY;q>0;q--)); do echo -en "\e[0K\r`date`: waiting...$q"; sleep 1; done
  for ((q=$REFRESH_DELAY;q>0;q--)); do sleep 1; done
done
