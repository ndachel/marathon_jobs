import requests
import sys
import json



##################
## list globals ##
##################
app_list = []
ip_list = []
ports_list = []
config_str = ''

##########################
## recursive json parse ##
##########################

def get_all(in_list, myjson, key):
    if type(myjson) == str:
        myjson = json.loads(myjson)
    if type(myjson) is dict:
        for jsonkey in myjson:
            if type(myjson[jsonkey]) in (list, dict):
                get_all(in_list, myjson[jsonkey], key)
            elif jsonkey == key:
  		in_list.append(myjson[jsonkey])
    elif type(myjson) is list:
        for item in myjson:
            if type(item) in (list, dict):
                get_all(in_list, item, key)

def get_all_list(in_list, myjson, key):
    if type(myjson) == str:
        myjson = json.loads(myjson)
    if type(myjson) is dict:
        for jsonkey in myjson:
            if type(myjson[jsonkey]) == dict:
                get_all_list(in_list, myjson[jsonkey], key)
            elif type(myjson[jsonkey]) == list:
 	        if jsonkey == key:
		    in_list.append(myjson[jsonkey])
                else:
	            get_all_list(in_list, myjson[jsonkey], key)
            elif jsonkey == key:
                in_list.append(myjson[jsonkey])
    elif type(myjson) is list:
        for item in myjson:
            if type(item) in (list, dict):
                get_all_list(in_list, item, key)

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

url = 'http://172.16.1.16:2379/v2/keys/apps/'
resp = requests.get(url)
active_apps = []
if resp.status_code != 200:
    # Something is wrong
    print('Error getting etcd apps list: ' + resp.text)
    print('Quitting')
    sys.exit()

from_json(active_apps, resp.json(), 'key','leaf')
active_len = len(active_apps)
for i in range(0,active_len):
    active_apps[i] = '/' + active_apps[i].strip('/apps').encode('ascii')    

print active_apps


url = 'http://marathon.mesos:8080/v2/tasks'

resp = requests.get(url)
if resp.status_code != 200:
    # Something is wrong
    print('GET /v2/task error: '  + resp.text)
    print('Quitting')
    sys.exit()

from_json(app_list,   resp.json(), 'appId', 'leaf')
from_json(ip_list,    resp.json(), 'host',  'leaf')
from_json(ports_list, resp.json(), 'ports', 'list')
print "Apps: {}  IPs: {} Ports: {}".format(len(app_list),len(ip_list),len(ports_list))
curr_app = ''
k = 1
for i in range(0,len(app_list) -1):
    next_app = app_list[i]
    if (next_app <> curr_app) & (next_app in active_apps):
        k = 1
        curr_app = next_app
        config_str = config_str +  '\n\nbackend ' + app_list[i]
        config_str = config_str +  '\n    balance   roundrobin'
        config_str = config_str +  '\n    mode      http'
       
    k = k + 1
    config_str = config_str +  '\n    server  app{} {}:{} check'.format(k, ip_list[i], str(ports_list[i]).strip('[]') )


print config_str
