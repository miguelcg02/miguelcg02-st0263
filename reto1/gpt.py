from flask import Flask, jsonify

class Nodo:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/joinNetwork/<ip>/<port>', methods=['GET'])
        def join_network(ip, port):
            self.send_join_request(ip, int(port))
            return jsonify({"status": "success join"})

    def send_join_request(self, ip, port):
        # Implementa la lógica para enviar una solicitud de unión a la red
        print(f"Sending join request to {ip}:{port}")

    def run(self):
        self.app.run(host='0.0.0.0', port=self.port)

# Crear una instancia de la clase Nodo y ejecutar la aplicación Flask
nodo_instance = Nodo('localhost', 5000)
nodo_instance.run()
