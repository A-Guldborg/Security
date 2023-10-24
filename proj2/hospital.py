import struct
import threading

from communication import serve_on_port

class Hospital:
    def __init__(self, port):
        self.port = port
        self.values = []
        threading.Thread(target=self.serve, daemon=False).start()
    
    def serve(self):
        sock = serve_on_port(self.port)
        
        for _ in range(3):
            client_tls_socket, _ = sock.accept()
            
            bytes = client_tls_socket.recv(4)
            self.rec_value(struct.unpack("!i", bytes)[0])
            client_tls_socket.close()
            
    # Receiving values from people
    def rec_value(self, value):
        print("Hospital: Received", value)
        self.values.append(value)
        if len(self.values) == 3:
            print("Hospital: Received three values with aggregate sum", sum(self.values))