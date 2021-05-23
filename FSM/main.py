from automata.fa.dfa import DFA
import socket
import numpy as np
stts=['AF','AR','BF','BR','CF','CR','DF','DR']
stdct={'A':'AF','B':'AR','C':'BF','D':'BR','E':'CF','F':'CR','G':'DF','H':'DR'}
inpdig={str(i) for i in range(1000)}
inpalp=['A','B','C','D','E','F','G','H']
kk={'AF':'AFAR','AR':'CFAR','BF':'BFBR','BR':'DFBR','CF':'CFCR','CR':'BFCR','DF':'CFDF','DR':'AFDR'}
tt={'AFAR':'A','CFAR':'B','BFBR':'C','DFBR':'D','CFCR':'E','BFCR':'F','CFDF':'G','AFDR':'H'}
host='127.0.0.1'
port=6553
for i in inpdig:
    stdct[i]='Start'
def trns1(x):
    retdct1={}
    for i in range(1000):
        retdct1[str(i)]=x
    for i in inpalp:
        retdct1[i]='Start'
    return retdct1
def trns(x):
    retdct={}
    for i in range(1,1000):
        retdct[str(i)]=kk[x]
    if(stts.index(x)==len(stts)-1):
        retdct['0']=stts[0]
    else:
        retdct['0']=stts[stts.index(x)+1]
    for i in inpalp:
        retdct[i]='Start'
    return(retdct)
from automata.fa.dfa import DFA
dfa=DFA(states={'Start','AF','AR','BF','BR','CF','CR','DF','DR','AFAR','CFAR','BFBR','DFBR','CFCR','BFCR','CFDF','AFDR'},
        input_symbols={'A','B','C','D','E','F','G','H'}.union(inpdig),
        transitions={
            'Start':stdct,
            'AF':trns('AF'),
            'AR':trns('AR'),
            'BF':trns('BF'),
            'BR':trns('BR'),
            'CF':trns('CF'),
            'CR':trns('CR'),
            'DF':trns('DF'),
            'DR':trns('DR'),
            'AFAR':trns1('AFAR'),
            'CFAR':trns1('CFAR'),
            'BFBR':trns1('BFBR'),
            'DFBR':trns1('DFBR'),
            'CFCR':trns1('CFCR'),
            'BFCR':trns1('BFCR'),
            'CFDF':trns1('CFDF'),
            'AFDR':trns1('AFDR')
        },
        initial_state='Start',
        final_states={'AFAR','CFAR','BFBR','DFBR','CFCR','BFCR','CFDF','AFDR'}
        )
tim=0
ServerSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    ServerSocket.bind((host,port))
except socket.error as e:
    print(str(e))


print('waiting for connection...')
ServerSocket.listen()

Client, address=ServerSocket.accept()

print('connected to: '+ address[0]+':'+str(address[1]))

Client.send(str.encode('enter'))


def takeinp():
    ctr=0
    while True:
        data = Client.recv(2048)
        reply = data.decode('utf-8')
        if not data and ctr!=0:
            break
        if not data and ctr==0:
            continue
        return reply

t=int(takeinp())


inistt='A'


timestamp=0
que=np.array([0 for i in range(8)])
def updateq(a,b):
    b=list(b)
    r1=b[0]
    r2=b[2]
    o1=b[1]
    o2=b[3]
    sstttrrr='ABCD'
    i1=sstttrrr.index(r1)
    i2=sstttrrr.index(r2)
    if(o1=='F'):
        t1=0
    if(o1=='R'):
        t1=1
    if(o2=='F'):
        t2=0
    if(o2=='R'):
        t2=1
    a[i1*2+t1]-=1
    a[i2*2+t2]-=1
    for i in range(len(a)):
        if(a[i]<0):
            a[i]=0
    return a
integerconvert=lambda x:int(x)
vfunc=np.vectorize(integerconvert)
while True:
    print('--------------------------------------------------\ntimestep: '+str(tim+1))
    if(tim<t):
        inpt=vfunc(np.array(takeinp().split(' ')))
        que=que + inpt
        print('input at t={}= {}'.format(tim+1,inpt))
    questr=''
    print('initial queue: {}'.format(que))
    for i in que:
        questr=questr+str(i)
    inii=inpalp.index(inistt)
    linsnd=inistt+questr[inii:]+questr[0:inii]
    state=dfa.read_input(linsnd)
    que=updateq(que,state)
    print('traffic signal state: {}'.format(state))
    print('final queue: {}\n-------------------------------------'.format(que))
    if(inpalp.index(tt[state])<len(inpalp)-1):
        inistt=inpalp[inpalp.index(tt[state])+1]
    else:
        inistt=inpalp[0]
    endingbool=True
    for i in que:
        if(i!=0):
            endingbool=False
    if(endingbool):
        break
    tim+=1
