from random import randint
import struct
import time

from communication import serve_on_port, connect

class Person:
    def __init__(self, name, port):
        self.port = port
        self.name = name
        self.received_values = []
        self.height = randint(150,210) # generate random height
        print(f'{name}: My (secret) height is', self.height)
        self.values_to_send = self.split_into_n(self.height, 3)
        
    
    def split_into_n(self, value, n):
        vals = []
        for _ in range(n-1):
            val = randint(0, value)
            vals.append(val)
            value -= val
            
        self.received_values.append(value) # add remaining value to own values array

        return vals 
        
    def serve(self):
        server_socket = serve_on_port(self.port)
                
        # Receive from 2 other people, could be n for scalability
        for _ in range(2):
            # Accept incoming connections
            client_tls_socket, _ = server_socket.accept()
                        
            incoming_bytes = client_tls_socket.recv(4)
            
            # Each connection is only responsible for sending one value
            client_tls_socket.close()
            
            incoming_value = struct.unpack("!i", incoming_bytes)[0]
            self.received_values.append(incoming_value)
        
        self.send_aggregate_value()

    # Send sum of all values to hospital
    def send_aggregate_value(self):
        aggregate_value = sum(self.received_values)
        print(f'{self.name}: I have calculated the aggregate value',  aggregate_value)

        hospital = connect(9000)
        
        # Convert int to ReadableBuffer
        data = struct.pack("!i", aggregate_value)
        hospital.send(data)
        
        # Allow time for server to receive data before closing socket from client side
        time.sleep(1)
        hospital.close()
    
    # Send part of height to two other people
    def send_values(self, receivers):        
        # Broadcast v1 to receiver1, v2 to receiver2 etc
        for idx, receiver in enumerate(receivers):
            print(f'{self.name}: Sending {self.values_to_send[idx]} to port {receiver}')
            socket = connect(receiver)
            
            # Convert integer to byte
            byte_value = struct.pack("!i", self.values_to_send[idx])
            
            socket.send(byte_value)
            
            # Give peer person time to receive data before closing socket from client_side
            time.sleep(1)
            socket.close()
