#!/usr/bin/env python3

import requests
import json
import jinja2


consul_server='http://127.0.0.1:8500'

lists=[]

try:
    s = requests.get(consul_server + '/v1/catalog/services', timeout = 3)
except:
    print ('Connect consul error.')
    exit(1)

svc_info = json.loads(s.text)

for svc_name in svc_info:
    ip_lists=[]
    nodes=[]

    try:
        n = requests.get(consul_server + '/v1/catalog/service/' + svc_name, timeout = 3)
    except:
        print ('Connect consul error.')
        exit(1)

    node_info = json.loads(n.text)

    for i in node_info:
        nodes.append(i['Node'])
        ip_lists.append(i['Address'])
    
    # print (nodes, ip_lists)

    lists.append(dict(groups_name=svc_name, hostname=nodes, ip=ip_lists))
    # print(lists)

loader = jinja2.FileSystemLoader('host.jinja2')
env = jinja2.Environment(loader=loader)
env.globals.update(zip=zip)
template = env.get_template('')

# print (template.render(items=lists))


with open('host', 'w') as configfile:
    configfile.write(template.render(items=lists))
