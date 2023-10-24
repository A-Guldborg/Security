
import socket
import ssl


# Hosting a server (server-side)
def serve_on_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", port))
    sock.listen(5)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
    
    return context.wrap_socket(sock)

# Connecting to a server (client-side)
def connect(port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) 
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect(("localhost", port))
    
    return context.wrap_socket(sock, server_hostname="localhost")