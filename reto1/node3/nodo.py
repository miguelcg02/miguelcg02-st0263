from flask import Flask, jsonify, request
import json
from dht import create_node

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

@app.route('/update_predecessor/<new_predecessor_id>/<new_predecessor_ip>/<new_predecessor_port>/', methods=['POST'])
def post_update_predecessor(new_predecessor_id,new_predecessor_ip,new_predecessor_port):
    node.update_predecessor(new_predecessor_id,new_predecessor_ip,new_predecessor_port)
    return jsonify({"message": "Joined the network",})

@app.route('/update_successor/<new_successor_id>/<new_successor_ip>/<new_successor_port>/', methods=['POST'])
def post_update_successor(new_successor_id,new_successor_ip,new_successor_port):
    node.update_successor(new_successor_id,new_successor_ip,new_successor_port)
    return jsonify({"message": "Joined the network",})

@app.route('/find_predecessor_bootstrap', methods=['GET'])
def get_find_predecessor_bootstrap():
    return jsonify({"id": node.predecessor.id,"ip":node.predecessor.ip, "port": node.predecessor.port})

@app.route('/leave', methods=['GET'])
def post_leave():
    node.leave_network()
    return jsonify({"message": "Left the network",})

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
    
    app.run(host=config["ip"], port=config["port"])

if __name__ == "__main__":
    main()
