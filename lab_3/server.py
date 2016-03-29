#!/usr/bin/env python2.7

import socket
import thread
import oarg

class Server(object):
    def __init__(self, host, port, recv_buffer=4096):
        self.connections = []
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        #starting socket
        self.start_socket()
        #listening
        self.listen()

    def start_socket(self):
        #creating socket    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        #use already occupied address
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #binding 
        self.socket.bind((self.host, self.port))

    def listen(self, backlog=16):
        #becoming a server
        self.socket.listen(backlog)

    def main_loop(self):
         while True:
            client_socket, client_address = self.socket.accept()
            print "address:", client_address
            self.connections.append((client_socket, client_address))
            thread.start_new(chat, (len(self.connections)-1, self,
                client_socket)) 

    def broadcast(self, data):
        print data
        for (client_socket, __) in self.connections:
            client_socket.sendall(data) 

    def __del__(self):
        self.socket.close()

def chat(thr_id, server, client_socket, recv_buffer=4096):
    while True:
        data = client_socket.recv(recv_buffer)
        server.broadcast("message from #%d: %s" % (thr_id, data))

def main():
    port = oarg.Oarg("-p --port", 1234, "port to start server")
    host = oarg.Oarg("-h --host", "", "host to start server")
    recv_buffer = oarg.Oarg("-b --buffer", 4096, "receiver buffer size")
    hlp = oarg.Oarg("--help", False, "this help message")

    oarg.parse()

    if hlp.val:
        oarg.describeArgs("options:")
        exit()

    print "starting server ..."
    server = Server(host.val, port.val, recv_buffer.val)
    print "started server on port #%d" % server.port

    print "starting server main loop"
    server.main_loop()

if __name__ == "__main__":
    main()
