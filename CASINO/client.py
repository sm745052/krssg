import socket
ClientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host='127.1.1.0'
port = 4776
x=input('enter number of players\n')
n=input('enter number of rounds\n')
print('waiting...')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
print('connected successfully')
ClientSocket.send((n+':'+x).encode('utf-8'))
print('done :)')