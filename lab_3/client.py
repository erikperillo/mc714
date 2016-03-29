#!/usr/bin/env python2.7

import socket
import oarg

def main():
    port = oarg.Oarg("-p --port", 1234, "server port")
    host = oarg.Oarg("-h --host", "", "server host")
    recv_buffer = oarg.Oarg("-b --buffer", 4096, "receiver buffer size")
    hlp = oarg.Oarg("-h --help", False, "this help message")

    oarg.parse()

    if hlp.val:
        oarg.describeArgs("options:")
        exit()

    server_address = (host.val, port.val)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    client_socket.sendall("")
    #data = client_socket.recv(recv_buffer.val)

    client_socket.close()

    print 'received:', data

if __name__ == "__main__":
    main()
