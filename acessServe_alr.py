import time
import socket
import binascii


class AcessServe_alr():
 
    host = ""
    porta = 0
    sock = socket.socket()
    
    def __init__(self, host = str('192.168.100.8'), porta = 3040):
        self.host = host
        self.porta = ":" + str(porta)
        pass
        
    def envia_servico(self, data_json):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, 3040))

        
        content_length = len(data_json)
        print("TAM ", len(data_json))
        headers = ("POST /envio HTTP/1.1\r\nContent-Type: {}\r\nContent-Length: {}\r\nHost: {}\r\nAccept: */*\r\nConnection: close\r\n\r\n").format("application/json", content_length, (self.host+self.porta)).encode()

        payload = headers + (data_json + "\r\n").encode()
        print(payload)
                 
        
        self.sock.sendall(payload)
        payload = 0
        print("######################################\n######################################")
        response = self.sock.recv(14096)
        print(response.decode())
        
        self.sock.close()

