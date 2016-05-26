import requests
import sys
import json
import fileinput

##################
## some globals ##
##################
app_list = []
ip_list = []
ports_list = []
config_str = ''

##########################
## recursive json parse ##
##########################
def from_json(in_list, myjson, key, in_type):
  if type(myjson) == str:
    myjson = json.loads(myjson)
  if type(myjson) is dict:
    for jsonkey in myjson:
      if type(myjson[jsonkey]) == dict:
        from_json(in_list, myjson[jsonkey], key, in_type)
      elif type(myjson[jsonkey]) == list:
        if (in_type == 'list'):
          if jsonkey == key:
            in_list.append(myjson[jsonkey])
          else:
            from_json(in_list, myjson[jsonkey], key, in_type)  
        elif (in_type == 'leaf'):
            from_json(in_list, myjson[jsonkey], key, in_type)
      elif jsonkey == key:
        in_list.append(myjson[jsonkey])
  elif type(myjson) is list:
    for item in myjson:
      if type(item) in (list, dict):
        from_json(in_list, item, key, in_type)

##########################
## Make a get rest call ##
##########################
def rest_get(url):
  resp = requests.get(url);
  if resp.status_code != 200:
    ### Something went wrong! ###
    print "Error getting {}!\n {}".format(url,resp.text)
    print "Quitting"
    sys.exit()
  else:
    return resp

#################################
## get balanced apps from etcd ##
#################################
response = rest_get('http://172.16.1.16:2379/v2/keys/apps/')

active_apps = []
from_json(active_apps, response.json(), 'key','leaf')
active_len = len(active_apps)
for i in range(0,active_len):
  active_apps[i] = '/' + active_apps[i].strip('/apps').encode('ascii')    

#################################
## get instances from marathon ##
#################################
response = rest_get('http://marathon.mesos:8080/v2/tasks')

# Get App IDs, host IP, and ports from API json
from_json(app_list,   response.json(), 'appId', 'leaf')
from_json(ip_list,    response.json(), 'host',  'leaf')
from_json(ports_list, response.json(), 'ports', 'list')

# loop marathon apps, and if a match to balanced app in etcd, make an haproxy config for it
curr_app = ''
k = 1
for i in range(0,len(app_list)):
  next_app = app_list[i]
  if (next_app <> curr_app) & (next_app in active_apps):
    k = 0
    curr_app = next_app

    ################################
    ## Get port from etcd for app ##
    ################################
    response = rest_get("http://172.16.1.16:2379/v2/keys/apps/{}/port".format(curr_app))
    port = []
    from_json(port, response.json(), 'value', 'leaf')

    # write frontend
    config_str = config_str + '\n\nfrontend ' + app_list[i].strip('/')
    config_str = config_str + '\n    bind 0.0.0.0:' + port[0].encode('ascii')
    config_str = config_str + '\n    default_backend ' + app_list[i].strip('/')
    config_str = config_str + '\n'

    # write backend
    config_str = config_str +  '\n\nbackend ' + app_list[i].strip('/')
    config_str = config_str +  '\n    balance   roundrobin'
    config_str = config_str +  '\n    mode      http'
    config_str = config_str + '\n    server app{} {}:{} check'.format(k, ip_list[i], str(ports_list[i]).strip('[]'))
  elif (next_app <> curr_app) & (next_app not in active_apps):
    curr_app = ''
  elif (curr_app in active_apps):       
    k = k + 1
    config_str = config_str + '\n    server app{} {}:{} check'.format(k, ip_list[i], str(ports_list[i]).strip('[]'))

config_str = config_str + '\n'

###############################################
## Copy the config into the haproxy template ##
###############################################
f = open('/var/lib/haproxy/haproxy.cfg.template','r')
template = f.read()
f.close()

config = template.replace("{{MARATHONAPPS}}",config_str)

f = open('/var/lib/haproxy/haproxy.cfg','w')
f.write(config)
f.close

