#!/usr/bin/env python2.7

import socket
import thread
import oarg

class Server(object):
    """
    class representing chat server.
    the server's main function is to receive incomming connections and
    broadcast them to all other clients.
    """
    def __init__(self, host, port, recv_buffer=4096):
        """
        variables initialization and socket setup.
        """
        self.connections = []
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        #starting socket
        self.start_socket()
        #listening
        self.listen()

    def start_socket(self):
        """
        starts socket with apropriate configurations.
        """
        #creating socket    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        #use already occupied address
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #binding 
        self.socket.bind((self.host, self.port))

    def listen(self, backlog=16):
        """
        sets up socket to become a server.
        """
        #becoming a server
        self.socket.listen(backlog)

    def main_loop(self):
        """
        main server loop where server receives connections and spams them
        to worker threads were it handles messages.
        """
        while True:
            client_socket, client_address = self.socket.accept()
            print " --- new connection to %s, port %d ---" % \
                (client_address[0], client_address[1])
            self.connections.append((client_socket, client_address))
            #worker thread
            thread.start_new(chat, (len(self.connections)-1, self,
                client_socket)) 

    def broadcast(self, data):
        """
        sends message to all connected clients.
        """
        print data
        for i, (client_socket, address) in enumerate(self.connections):
            try:
                client_socket.sendall(data) 
            except Exception as e:
                print " --- connection error in socket #%d: %s ---" % \
                    (i, e.message)
                client_socket.close()
                self.connections.remove((client_socket, address))

    def __del__(self):
        for (client_socket, __) in self.connections:
            client_socket.close()
        self.socket.close()

def chat(thr_id, server, client_socket, recv_buffer=4096):
    """
    connetion handler: each connection spams a thread that calls this 
    function.
    """
    while True:
        try:
            data = client_socket.recv(recv_buffer)
            if data:
                server.broadcast(" ---> message from #%d: %s <---" \
                    % (thr_id, data))
        except:
            break

def main():
    #command line arguments
    port = oarg.Oarg("-p --port", 5050, "port to start server")
    host = oarg.Oarg("-h --host", "", "host to start server")
    recv_buffer = oarg.Oarg("-b --buffer", 4096, "receiver buffer size")
    hlp = oarg.Oarg("--help", False, "this help message")

    oarg.parse()

    if hlp.val:
        oarg.describeArgs("options:")
        exit()

    print " --- starting server ---"
    server = Server(host.val, port.val, recv_buffer.val)
    print " --- started server on port %d ---" % server.port

    print " --- starting server main loop ---"
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print " --- service terminated ---"  
        exit()

if __name__ == "__main__":
    main()
