#!/usr/bin/env python2.7

import socket
import thread
import oarg
import time
import sys

class Client(object):
    def __init__(self, server_host, server_port, recv_buffer=4096):
        self.server_host = server_host
        self.server_port = server_port
        self.recv_buffer = recv_buffer
        #starting socket
        self.start_socket()
        #connecting to server
        self.connect_to_server()

    def start_socket(self):
        #creating socket    
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        #use already occupied address
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect_to_server(self):
        self.server_socket.connect((self.server_host, self.server_port))

    def main_loop(self):
        thread.start_new(listener, (self.server_socket,))
        while True:
            data = raw_input("insert message: ")
            self.server_socket.sendall(data)

    def __del__(self):
        self.socket.close()

def listener(socket, recv_buffer=4096):
    while True:
        #sys.stdout.write("insert message: ")
        #sys.stdout.flush()
        data = socket.recv(recv_buffer)
        print data

def main():
    port = oarg.Oarg("-p --port", 1234, "server port")
    host = oarg.Oarg("-h --host", "", "server host")
    message = oarg.Oarg("-m --message", "ey b0ss", "message to send")
    hlp = oarg.Oarg("-h --help", False, "this help message")

    oarg.parse()

    if hlp.val:
        oarg.describeArgs("options:")
        exit()

    print "starting server ..."
    client = Client(host.val, port.val)
    print "conneted to", (client.server_host, client.server_port)

    print "starting server main loop"
    client.main_loop()

if __name__ == "__main__":
    main()
