import socket
import os
import threading
import random
import numpy as np 
import pandas as pd
import time
host='127.0.0.1'
port=6553
host1='127.1.1.0'
port1=4776


ServerSocket1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ServerSocket1.bind((host1,port1))
except socket.error as e:
    print(str(e))


print('waiting for connection...[client]')
ServerSocket1.listen()
clnt,ad=ServerSocket1.accept()
print('connected to client at {}'.format(ad))
ctr=0
while True:
    data = clnt.recv(2048)
    reply = data.decode('utf-8')
    if not data and ctr!=0:
        break
    if not data and ctr==0:
        continue
    ctr+=1
    no_of_rounds=int(reply.split(':')[0])
    no_of_players=int(reply.split(':')[1])
repchbool={i:False for i in range(no_of_players)}
repcheckend=[False for i in range(no_of_players)]
incomingthreads=[0 for i in range(no_of_players)]
def endsend(cnnctn):
    cnnctn.send(str.encode('end:'))
def repeatcheck(cnnctn,x):
    cnnctn.send(str.encode('repeat:?'))
    print('repeat Request sent to {}'.format(x))
    ctr=0
    while True:
        data = cnnctn.recv(2048)
        reply = data.decode('utf-8')
        if not data and ctr!=0:
            break
        if not data and ctr==0:
            continue
        print('{} replied {}'.format(x,reply))
        if(reply.lower()=='y'):
            repchbool[x]=True
        if(reply.lower()=='n'):
            repchbool[x]=False
        ctr+=1
        break
    repcheckend[x]=True

def sendresults(cnnctn, x):
    cnnctn.send(str.encode('finalwinners:'+str(x)))


return_dict={}
def sendcards(cnnctn,x,i,rnd): #sends elements of x to cnnctn
    cnnctn.send(str.encode('round:{}'.format(rnd)))
    cnnctn.send(str.encode('cards:'+str(x[0])+':'+str(x[1])+':'+str(x[2])))
    print('cards sent to {}'.format(i))
    ctr=0
    while True:
        data = cnnctn.recv(2048)
        reply = data.decode('utf-8')
        if not data and ctr!=0:
            break
        if not data and ctr==0:
            continue
        print('{} replied {}'.format(i,reply))
        return_dict[i]=int(reply)
        ctr+=1
        cnnctn.sendall(str.encode('recieved:'+reply))
        break
    threadcompletion[i]=True
ServerSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)



threadcompletion=[False for i in range(no_of_players)]
Client=[0 for i in range(no_of_players)]
address=[0 for i in range(no_of_players)]
joined=0

def value_of_card(x):
    if(x<=13):
        return x
    elif(x<=26):
        return x-13
    elif(x<=39):
        return x-26
    else:
        return x-39

try:
    ServerSocket.bind((host,port))
except socket.error as e:
    print(str(e))


print('waiting for connection...[players]')
ServerSocket.listen(no_of_players)


def threaded_client(connection,x):
    connection.send(str.encode('welcome: welcome to the server'))
    connection.send(str.encode('player:{}'.format(x)))

def find_winner():
    v=pd.Series(list(return_dict.values()))
    kd=v.apply(value_of_card)
    m=kd.max()
    winners=[]
    for i in range(len(kd)):
        if(m==kd[i]):
            for j in range(len(return_dict)):
                if(return_dict[j]==v[i]):
                    winners.append(j)
            break
    return winners
while (joined!=no_of_players):
    Client[joined], address[joined]=ServerSocket.accept()
    print('connected to: '+ address[joined][0]+':'+str(address[joined][1]))
    print(address[joined])
    incomingthreads[joined]=threading.Thread(target=threaded_client,args=(Client[joined],joined,))
    incomingthreads[joined].start()
    joined+=1
    print('join Number: '+str(joined-1))
for i in range(no_of_players):
    incomingthreads[i].join()
while True:
    print('\n------------------------------------------------------------\nOKAY!! Lets start the GAME')


    successrate=[0 for i in range(no_of_players)]
    presentround=1
    while(presentround<=no_of_rounds):
        
        suffle=random.sample(range(1,53),no_of_players*3)
        packs=[0 for i in range(no_of_players)]
        k=0
        t=0
        for ctrr in range (no_of_players):
            packs[t]=[suffle[k],suffle[k+1],suffle[k+2]]
            k=k+3
            t=t+1


        thread_objs=[0 for i in range(no_of_players)]


        for i in range(no_of_players):
            thread_objs[i]=threading.Thread(target=sendcards,args=(Client[i],packs[i],i,presentround,)) #see comma might be a problem
            thread_objs[i].start()
        
        boo=False
        while(not boo):
            bootemp=True
            for i in range(no_of_players):
                bootemp=bootemp and threadcompletion[i]
            boo=bootemp
        threadcompletion=[False for i in range(no_of_players)]
        winners=find_winner()
        for i in winners:
            successrate[i]=successrate[i]+1

        print(str(winners)+' won the round')
        print('-------------------------\nscore board\n'+str(successrate)+'\n-----------------------\n')
        presentround=presentround+1
    fin=pd.Series(successrate)
    m=fin.max()
    finwinners=[]
    for i in range(len(fin)):
        if(m==fin[i]):
            finwinners.append(i)
    print(finwinners)
    for i in range(no_of_players):
        thread_objs[i]=threading.Thread(target=sendresults,args=(Client[i],finwinners,)) #see comma might be a problem
        thread_objs[i].start()
    thread_objs[no_of_players-1].join()
    return_dict={}
    threading_for_repeat=[0 for i in range(no_of_players)]
    for i in range(no_of_players):
        threading_for_repeat[i]=threading.Thread(target=repeatcheck,args=(Client[i],i))
        threading_for_repeat[i].start()
    while(False in repcheckend):
        asd=0
    if(False in repchbool.values()):
        print('----------------------------\nthe end')
        for i in range(no_of_players):
            threading.Thread(target=endsend,args=(Client[i],)).start()
        break
    repchbool={i:False for i in range(no_of_players)}
    repcheckend=[False for i in range(no_of_players)]

ServerSocket.close()