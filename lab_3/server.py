#!/usr/bin/env python2.7

import socket
import thread
import oarg

def echo(index, client_socket, client_address, recv_buffer=4096):
    while True:
        data = server_socket.recv(recv_buffer)
        print "data:", data

def main():
    port = oarg.Oarg("-p --port", 1234, "port to start server")
    host = oarg.Oarg("-h --host", "", "host to start server")
    recv_buffer = oarg.Oarg("-b --buffer", 4096, "receiver buffer size")
    hlp = oarg.Oarg("-h --help", False, "this help message")

    oarg.parse()

    if hlp.val:
        oarg.describeArgs("options:")
        exit()

    #address of server (reachable by any address the machine has)
    server_address = (host.val, port.val)

    #list of clients connected to server
    connections = []

    #creating socket    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    #binding 
    server_socket.bind(server_address)
    #becoming a server
    server_socket.listen(1)

    print "started server on port #%d" % port.val

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print "connected by", client_address
            connections.append((client_socket, client_address))
            data = client_socket.recv(recv_buffer.val)
            print "data:", data 
    except KeyboardInterrupt:
        print "server finished"

if __name__ == "__main__":
    main()
