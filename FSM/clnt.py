import socket
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 6553
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
    print('connected')
except socket.error as e:
    print(str(e))
def takeinp():
    ctr=0
    while True:
        data = ClientSocket.recv(2048)
        reply = data.decode('utf-8')
        if not data and ctr!=0:
            break
        if not data and ctr==0:
            continue
        return reply
while True:
    inp=takeinp()
    if(len(inp)>0):
        print(inp)
    mssg=input()
    ClientSocket.send(mssg.encode('utf-8'))
    t=int(mssg)
    for i in range(t):
        mssg=input()
        ClientSocket.send(mssg.encode('utf-8'))