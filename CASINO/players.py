import socket
import pandas as pd
import time
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 6553


def value_of_card(x):
    if(x<=13):
        return x
    elif(x<=26):
        return x-13
    elif(x<=39):
        return x-26
    else:
        return x-39

plrno=-1
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
while True:
    Response = (ClientSocket.recv(2048)).decode('utf-8')
    header=Response.split(':')[0]
    payload=Response.split(':')[1:]
    if(header=='welcome'):
        print((payload[0]))
    elif(header=='recieved'):
        print('value of card sent successfully: '+payload[0])
    elif(header=='player'):
        plrno=int(payload[0])
        print('player number: '+ str(plrno))
    elif(header=='cards'):
        time.sleep(.1)
        print('your cards are: '+str(payload))
        valpay=((pd.Series(payload).apply(lambda x:int(x))).apply(value_of_card))
        m=valpay.max()
        print('sent: '+str(((pd.Series(payload).apply(lambda x:int(x)))[((pd.Series(payload).apply(lambda x:int(x))).apply(value_of_card))==m]).tolist()[0]))
        ClientSocket.send(str.encode(str(m)))
    elif(header=='finalwinners'):
        print('------------------------------------')
        print('winners are'+str(payload[0]))
        if(str(plrno) in payload[0]):
            print('congo wohooo!!!!')
        else:
            print('koi naa !!')
        print('------------------------------------')
    elif(header=='repeat'):
        while True:
            print('U want to continue? [Y/n]')
            ans=input()
            if(ans.lower()=='y'):
                break
            if(ans.lower()=='n'):
                print('This will end the game for all players. You want to continue to end? [Y/n]')
                ans1=input()
                if(ans1.lower()=='y'):
                    break
        ClientSocket.send(str.encode(ans))
    elif(header=='end'):
        print('------------------------\nGame Ended T_T')
        break
    elif(header=='round'):
        rnd=payload[0]
        print('---------------------------------------------\nround: {}\n------------------------------------'.format(rnd))
    else:
        if Response:
            print('elseblock: '+Response)
ClientSocket.close()
