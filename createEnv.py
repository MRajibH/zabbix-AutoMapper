#!/usr/bin/python3
import random

from zabbix_utils import ZabbixAPI

# Zabbix server details
zabbix_url = "http://192.168.31.9:8080/"
api = ZabbixAPI(url=zabbix_url)
api.login(token="cd5480fb1ab2b07379a87fa96d12acd676935d93f15d6c9d5baa2b8ca54b0c38")


def create_host_group(host_group_name):
    result = api.hostgroup.create({
        "name": host_group_name
    })

    return result["groupids"][0]


def create_host(host_name, type="server", link="", host_group="",ip="",link_label=""):
    result = api.host.create({
        "host": host_name,
                "templates": [
            {
                "templateid": "10343"
            }
        ],
        "interfaces": [
            {
                "type": 1,
                "ip": ip,
                "dns": "",
                "port": "10050",
                "useip": 1,
                "main": 1
            }
        ],
        "tags": [
            {
                "tag": "am.link.connect_to",
                "value": link
            },
            {
                "tag": "am.link.color",
                "value": "00ff00"
                # "value": random.choice(["00ff00","4000FF","FFBF00","FF4000","FF0000"])
            },
            {
                "tag": "am.link.draw_type",
                # "value": str(random.randint(1, 4))
                "value": "1"
            },
            {
                "tag": "am.link.label",
                # "value": str(random.randint(1, 4))
                "value": link_label
            },
            {
                "tag": "am.host.type",
                "value": type
            }
        ],
        "groups": [{
            "groupid": host_group
        }]
    })
    return result

def get_list_hosts_from_host_group(hostgroup_id):
    hosts = api.host.get({
        "groupids": hostgroup_id,
        "output": ["hostid"]
    })
    return hosts

def delete_hosts_from_host_group(hostgroup_id):
    hosts = get_list_hosts_from_host_group(hostgroup_id)
    host_array=[host["hostid"] for host in hosts]

    result = api.host.delete(*host_array)

    return True


host_group_id = 22
#delete_hosts_from_host_group(host_group_id)

for i in range(1, 41):
    host_type = "server"
    host_name = f"Linux server {i}"
    link = f"switch {random.randint(1, 10)}"
    link_label = "NET : {?last(/"+link+"/net.utilization)}"
    result = create_host(host_name, host_type, link, host_group_id,f"10.10.10.{i}")
    print(f"Created host: {host_name}  {host_type} {link} - Result: {result}")

for i in range(1, 11):
    host_type = "switch"
    link = f"router {random.randint(1, 5)}"
    host_name = f"switch {i}"
    link_label = "NET : {?last(/"+link+"/net.utilization)}"
    result = create_host(host_name, host_type, link, host_group_id,f"10.10.20.{i}",link_label=link_label)
    print(f"Created host: {host_name}  {host_type} {link}- Result: {result}")

for i in range(1, 6):
    host_type = "router"
    link = f"router {random.randint(1, 5)}"
    host_name = f"router {i}"
    link_label = "NET : {?last(/"+link+"/net.utilization)}"
    result = create_host(host_name, host_type, link, host_group_id,f"10.10.30.{i}",link_label=link_label)
    print(f"Created host: {host_name}  {host_type} {link}- Result: {result}")
