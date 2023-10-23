
import socket
import ssl


def serve_on_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", port))
    sock.listen(5)
    
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
    
    return context, sock

def connect(port):
    context = ssl.create_default_context()
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")    
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", port))
    return sock # Without SSL
    return context.wrap_socket(sock)

