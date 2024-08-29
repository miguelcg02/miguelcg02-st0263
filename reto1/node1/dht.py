# common/dht.py
import hashlib
from utils import get_hash
import requests

# common/dht.py

class Node:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.successor = None
        self.predecessor = None

    def join_network(self, bootstrap_node, config):
        if config.get("bootstrap_port") == config.get("port"):
            # El primer nodo se convierte en el nodo bootstrap
            print("El primer nodo se convierte en el nodo bootstrap")
            self.successor = self
            self.predecessor = self
            self.successor.port = config.get("port") 
            self.predecessor.port = config.get("port")

            print(f"Node {self.id} is now the bootstrap node.")
        else:
            # El nuevo nodo se une al anillo
            print("El nuevo nodo se une al anillo")
            self.successor = bootstrap_node
            
            # Pregunta por cual era el antecesor del bootsrap para que se convierta en su antecesor
            reponse = requests.get(f"http://{bootstrap_node.ip}:{bootstrap_node.port}/find_predecessor_bootstrap")
            self.predecessor = Node(reponse.json()["id"],reponse.json()["ip"],reponse.json()["port"])
            
            # Si pasa, significa que es el segundo nodo y debe mandar a actualizar el predecesor del nodo bootstrap (siempre el nodo bootsrap es el sucesor del actual)
            if self.successor.id == self.predecessor.id:
                requests.post(f"http://{self.successor.ip}:{self.successor.port}/update_successor/", json={'successor_id':self.id,'successor_ip':self.ip,'successor_port':self.port})
            else:
                requests.post(f"http://{self.predecessor.ip}:{self.predecessor.port}/update_successor/", json={'successor_id':self.id,'successor_ip':self.ip,'successor_port':self.port})

            # Debo asignarle al bootstrap cual su nuevo antecesor
            requests.post(f"http://{self.successor.ip}:{self.successor.port}/update_predecessor/", json={'predecessor_id':self.id,'predecessor_ip':self.ip,'predecessor_port':self.port})
        
        # Mostrar la información del nodo
        self.print_node_info()
    
    def update_predecessor(self, new_predecessor_id,new_predecessor_ip,new_predecessor_port):
        self.predecessor = Node(new_predecessor_id,new_predecessor_ip,new_predecessor_port)

    def update_successor(self, new_successor_id,new_successor_ip,new_successor_port):
        self.successor = Node(new_successor_id,new_successor_ip,new_successor_port)

    def leave_network(self):
        requests.post(f"http://{self.predecessor.ip}:{self.predecessor.port}/update_successor/", json={'successor_id':self.successor.id,'successor_ip':self.successor.ip,'successor_port':self.successor.port})
        requests.post(f"http://{self.successor.ip}:{self.successor.port}/update_predecessor/", json={'predecessor_id':self.predecessor.id,'predecessor_ip':self.predecessor.ip,'predecessor_port':self.predecessor.port})

    def print_node_info(self):
        pred_id = self.predecessor.id if self.predecessor else None
        succ_id = self.successor.id if self.successor else None
        print(f"Node {self.id} running at {self.ip}:{self.port}")
        print(f"Files: {self.get_files()}")
        print(f"Predecessor: {pred_id}")
        print(f"Successor: {succ_id}")

    def get_files(self):
        # Aquí puedes poner la lógica para recuperar los archivos
        return ["file1.txt", "file2.txt"]

def create_node(ip, port):
    id = get_hash(f"{ip}:{port}")
    return Node(id, ip, port)

