#!/usr/bin/python3
import threading
from flask import Flask, request, jsonify, json
from controller import openstack

ctl = None
node_mapping, vm_mapping, node_status = dict(), dict(), dict()
app = Flask(__name__)


def scheduler_func():
    #global vm_mapping
    #for k in vm_mapping:
    pass

@app.route('/update_node', methods=['POST'])
def update_node():
    global node_status
    # Get latency from each server via request
    # Get system info of each server from OpenStack
    new_status = {k: request.json[k] for k in ['latency', 'hostname', 'cpu', 'memory', 'disk_usage']}
    node_status[request.remote_addr] = new_status
    return jsonify({'status': "Succeed", 'info': node_status[request.remote_addr]})

@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    # Return a list of active servers
    return jsonify({'node_list': node_mapping.values()})


@app.route('/register', methods=['POST'])
def register_node():
    # Get internal and external IP address from edges
    # Store it in a database
    global node_mapping
    global node_status
    print(request.json)
    node_mapping[request.remote_addr] = request.json['public_ip']
    node_status[request.remote_addr] = {'hostname': request.json['hostname']}
    print(node_mapping)
    print(node_status)
    return jsonify({'status': "Succeed"})


@app.route('/client_connect', methods=['POST'])
def client_connect():
    global vm_mapping
    client = request.json['name']
    if client in vm_mapping and 'address' in vm_mapping[client]:
        resp = jsonify({'status': 'Succeed', 'address': vm_mapping[client]['address'], \
                'node_list': list(node_mapping.values())})
        resp.status_code = 200
        return resp

    ret, virtual_ip = ctl.map_to_instance(client)
    if (ret != 'Succeed') or (virtual_ip is None):
        return jsonify({'status': ret, 'reason': virtual_ip})

    vm_mapping[client] = {'address': virtual_ip}
    print(vm_mapping)
    print(vm_mapping.values())
    resp = jsonify({'status': 'Succeed', 'address': virtual_ip, \
            'node_list': list(node_mapping.values())}) # if len(node_mapping) > 0 else []})
    resp.status_code = 200
    return resp

def main():
    global ctl
    global ip_mapping
    # Initiate the controller object and server
    ctl = openstack.OpenStackController()
    # Initiate scheduler thread
    #scheduler = threading.Thread(target=schdule_func)
    #scheduler.start()
    app.run(host='0.0.0.0', debug=True, port='5001')


if __name__ == '__main__':
    main()
