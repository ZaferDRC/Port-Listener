import socket
import subprocess
import ipaddress
from argparse import ArgumentParser

class SocketServer:
    def __init__(self, host, port, max_data_size=1024):
        self.host = host
        self.port = port
        self.max_data_size = max_data_size
        self.validate_host()
        self.validate_port()

    def validate_host(self):
        try:
            ipaddress.ip_address(self.host)
        except ValueError:
            raise ValueError("Invalid Host IP Provided.")
            
    def validate_port(self):
        if self.port <= 0 or self.port > 65535:
            raise ValueError("Invalid Port Number Provided. Port Number Should Be Between 0 And 65535")
                
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

    def accept_connection(self):
        client_socket, client_addr = self.server_socket.accept()
        return client_socket, client_addr

    def receive_data(self, client_socket):
        data = client_socket.recv(self.max_data_size)
        return data

    def close_socket(self, client_socket):
        client_socket.close()

    def close_server(self):
        self.server_socket.close()

def create_figlet_text():
    text = subprocess.check_output(['figlet', 'PortEar'])
    print(text.decode('utf-8'))

def main(host, port):
    try:
        create_figlet_text()
        server = SocketServer(host, port)
        server.start()

        while True:
            client_socket, client_addr = server.accept_connection()
            print(f"Connection Accepted: {client_addr[0]}:{client_addr[1]}")
            data = server.receive_data(client_socket)
            if data:
                print(f"Incoming Data: {data.decode('utf-8')}")

            server.close_socket(client_socket)

    except Exception as error:
        print(f"An Unexpected Error Occurred: {error}")
    except KeyboardInterrupt:
        print("Program Stopped.")
    finally:
        try:
            server.close_server()
        except UnboundLocalError as error:
            print("An Unexpected Error Occurred: Socket Not Properly Initialized.")
        except Exception as error:
            print(f"An Unexpected Error Occurred: {error}")

if __name__ == "__main__":
    parser = ArgumentParser(description="Socket Server")
    parser.add_argument("--host", default="0.0.0.0", help="Server Host")
    parser.add_argument("--port", type=int, required=True, help="Server Port")
    args = parser.parse_args()

    main(args.host, args.port)
