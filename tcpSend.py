import socket
import sys

def Main(ip, port, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(data)
   
if __name__ == '__main__':
    arguments = str(sys.argv)
    ipHost = arguments[0]
    portHost = int(arguments[1])
    string = arguments[2]
    dataToSend = string.encode('utf-8')
    Main(ipHost, portHost, dataToSend)

