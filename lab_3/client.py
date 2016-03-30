#!/usr/bin/env python2.7

import socket
import thread
import oarg
import sys

class Client(object):
    """
    this class represent client side in the chat.
    it connects to the server and can send and receive messages.    
    """
    def __init__(self, server_host, server_port):
        """
        variables initialization and socket setup.
        """
        self.server_host = server_host
        self.server_port = server_port
        #starting socket
        self.start_socket()
        #connecting to server
        self.connect_to_server()

    def start_socket(self):
        """
        starts socket with apropriate configurations.
        """
        #creating socket    
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        #use already occupied address
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect_to_server(self):
        """
        starts connection with chat server.
        """
        self.server_socket.connect((self.server_host, self.server_port))

    def main_loop(self):
        """
        spams a thread to listen to messages from other clients and
        then keeps waiting for user input.
        """
        thread.start_new(listener, (self.server_socket,))
        while True:
            data = raw_input()
            self.server_socket.sendall(data)

    def __del__(self):
        self.server_socket.close()

def listener(socket, recv_buffer=4096):
    """
    worker thread calls this function to listen to other clients.
    """
    while True:
        sys.stdout.write(">>> ")
        sys.stdout.flush()
        data = socket.recv(recv_buffer)
        if not data:
            break
        print data

def main():
    #command line arguments
    port = oarg.Oarg("-p --port", 5050, "server port")
    host = oarg.Oarg("-h --host", "", "server host")
    hlp = oarg.Oarg("--help", False, "this help message")

    oarg.parse()

    if hlp.val:
        oarg.describeArgs("options:")
        exit()

    print " --- setting up client ---" 
    client = Client(host.val, port.val)
    print " --- conneted to server '%s', port %d ---" % \
        (client.server_host, client.server_port)

    print " --- starting client main loop. type as you wish! ---"
    try:
        client.main_loop()
    except Exception as e:
        print " --- connection error: '%s' --- " % e.message
        exit()

if __name__ == "__main__":
    main()
