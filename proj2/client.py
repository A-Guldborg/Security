from random import randint
import struct
import threading
import time

from communication import serve_on_port, connect

class Person:
    def __init__(self, name, port):
        self.port = port
        self.name = name
        self.values = []
        self.height = randint(150,210) # generate random height
        print(f'{name}: My (secret) height is', self.height)
    
    def split_into_n(self, value, n):
        vals = []
        for _ in range(n-1):
            val = randint(0, value)
            vals.append(val)
            value -= val
            
        self.values.append(value) # add remaining value to own values array

        return vals 
        
    def serve(self):
        ctx, server_socket = serve_on_port(self.port)
        
        print(f"{self.name}: Serving on {self.port}")
        
        # Receive from 2 other people, could be n for scalability
        for _ in range(2):
            # Accept incoming connections
            client_socket, _ = server_socket.accept()
            
            # Wrap sockets in TLS context
            # client_ssl_socket = ctx.wrap_socket(client_socket)
            
            incoming_bytes = client_socket.recv(4)
            
            # Each connection is only responsible for sending one value
            client_socket.close()
            
            incoming_value = struct.unpack("!i", incoming_bytes)[0]
            self.values.append(incoming_value)
        
        self.send_aggregate_value()

    # Send sum of all values to hospital
    def send_aggregate_value(self):
        aggregate_value = sum(self.values)
        print(f"TEST: Length of values for {self.name}: {len(self.values)}")
        print(f'{self.name}: I have calculated the aggregate value',  aggregate_value)

        hospital = connect(9000)
        
        # Convert int to ReadableBuffer
        data = struct.pack("!i", aggregate_value)
        hospital.send(data)
    
    # Send part of height to two other people
    def send_values(self, receivers):
        vals = self.split_into_n(self.height, len(receivers) + 1)
        
        # Broadcast v1 to receiver1, v2 to receiver2 etc
        for idx, receiver in enumerate(receivers):
            print(f'{self.name}: Sending {vals[idx]} to port {receiver}')
            socket = connect(receiver)
            
            # Convert integer to byte
            byte_value = struct.pack("!i", vals[idx])
            
            socket.send(byte_value)
