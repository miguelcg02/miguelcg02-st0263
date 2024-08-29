from flask import Flask, jsonify, request
import json
from dht import create_node
import requests

app = Flask(__name__)
node = None

def load_config():
    with open("config.json") as f:
        return json.load(f)

@app.route('/files', methods=['GET'])
def get_files():
    return jsonify(node.get_files())

@app.route('/info', methods=['GET'])
def get_info():
    return jsonify({"id": node.id, "predecessor": node.predecessor.id if node.predecessor else None, "successor": node.successor.id if node.successor else None})

@app.route('/update_predecessor/', methods=['POST'])
def post_update_predecessor():
    data = request.json
    new_predecessor_id = data["predecessor_id"]
    new_predecessor_ip = data["predecessor_ip"]
    new_predecessor_port = data["predecessor_port"]
    node.update_predecessor(new_predecessor_id,new_predecessor_ip,new_predecessor_port)
    return jsonify({"message": "Joined the network",})

@app.route('/update_successor/', methods=['POST'])
def post_update_successor():
    data = request.json
    new_successor_id = data["successor_id"]
    new_successor_ip = data["successor_ip"]
    new_successor_port = data["successor_port"]
    node.update_successor(new_successor_id,new_successor_ip,new_successor_port)
    return jsonify({"message": "Joined the network",})

@app.route('/find_predecessor_bootstrap', methods=['GET'])
def get_find_predecessor_bootstrap():
    return jsonify({"id": node.predecessor.id,"ip":node.predecessor.ip, "port": node.predecessor.port})

@app.route('/leave', methods=['GET'])
def post_leave():
    node.leave_network()
    return jsonify({"message": "Left the network",})

#http://127.0.0.1:5000/send_message/hola.txt/127.0.0.1/5001
@app.route('/send_message/<name_file>/<target_ip>/<target_port>', methods=['GET'])
def send_message(name_file,target_ip,target_port):
    # Enviar el mensaje al nodo objetivo
    print('Entré a send message')
    print('name_file:',name_file)
    print('target_ip:',target_ip)
    print('target_port:',target_port)
    response = requests.post(f"http://{target_ip}:{target_port}/receive_message/", json={'name_file':name_file,'sender_ip':node.ip,'sender_port':node.port})
    
    return jsonify({"status": "message sent", "response":'ok'})

@app.route('/receive_message/', methods=['POST'])
def receive_message():
    print('Entré a receive message')
    data = request.json
    name_file = data["name_file"]
    sender_ip = data["sender_ip"]
    sender_port = data["sender_port"]
    print('name_file:',name_file)
    print('sender_ip:',sender_ip)
    print('sender_port:',sender_port)
    
    return jsonify({"status": "message received", "message": 'ok'})

def main():
    global node
    config = load_config()
    node = create_node(config["ip"], config["port"])

    # El nodo bootstrap se maneja con bootstrap_node = None
    bootstrap_node = None
    if config.get("bootstrap_ip") and config.get("bootstrap_port"):
        bootstrap_node = create_node(config["bootstrap_ip"], config["bootstrap_port"])

    node.join_network(bootstrap_node, config)
    
    # La información del nodo se imprimirá al final de `join_network`
    
    app.run(host=config["ip"], port=config["port"], threaded=True)

if __name__ == "__main__":
    main()