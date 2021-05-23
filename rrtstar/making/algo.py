import cv2 as cv
import matplotlib.pyplot as plt
import math
import numpy as np
import random
import time
import pickle
import keyboard
random.seed(time.time())
img=cv.imread('1.png')
img1=cv.imread('1.png')
height, width = img.shape[:2]
imgray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh=cv.threshold(imgray,50,255,0)
contours,hierarchy=cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

dstncontours=[contours[0],contours[1],contours[11]]
strtcontours=[contours[4],contours[14],contours[15]]

obscontours=[]

for i in range(len(contours)):
    if( i not in [0,1,4,11,14,15]):
        obscontours.append(contours[i])


obscontours1=[list(i) for i in obscontours]                  #remember
obscontours1=[[[list(k) for k in i] for i in j] for j in obscontours1]


cv.imshow('xd',img)
cv.waitKey(0)
cv.drawContours(img, strtcontours,-1,(255,0,255), 1)
cv.imshow('xd',img)
cv.waitKey(0)
cv.drawContours(img, dstncontours,-1,(34,56,233), 2)
cv.imshow('xd',img)
cv.waitKey(0)
cv.drawContours(img, obscontours,-1,(56,200,233), 2)
cv.imshow('xd',img)
cv.waitKey(0)

strt=[255,0,255]
dstn=[34,56,233]
obs=[56,200,233]

obsx,obsy=np.where(np.all(img==obs,axis=2))
obscontours1=list(np.column_stack((obsy,obsx)))
obscontours1=[list(i) for i in obscontours1]

strtx,strty=np.where(np.all(img==strt,axis=2))
strtcontours1=list(np.column_stack((strty,strtx)))
strtcontours1=[list(i) for i in strtcontours1]


dstnx,dstny=np.where(np.all(img==dstn,axis=2))
dstncontours1=list(np.column_stack((dstny,dstnx)))
dstncontours1=[list(i) for i in dstncontours1]



parent={}
nodes={}

def create_node(x,y,nme,prnt):
    nodes[nme]=(x,y)
    parent[nme]=prnt

def rewiring(r):
    for i in list(nodes.keys()):
        for j in list(nodes.keys()):
            if(j==i):
                continue
            if abs(nodes[j][0]-nodes[i][0])<r and abs(nodes[j][1]-nodes[i][1])<r:
                if find_path_length(j)+len_bet_points(nodes[j][0],nodes[j][1],nodes[i][0],nodes[i][1])<find_path_length(i) and not obscolchk(nodes[j][0],nodes[j][1],nodes[i][0],nodes[i][1]):
                    print('------------------------')
                    parent[i]=j
        

def direct_len_bet_nodes(nme1,nme2):
    node1x=float(nodes[nme1][0])
    node1y=float(nodes[nme1][1])
    node2x=float(nodes[nme2][0])
    node2y=float(nodes[nme2][1])
    return(((node1x-node2x)**2+(node1y-node2y)**2)**.5)


def len_bet_points(x1,y1,x2,y2):
    return(((x1-x2)**2+(y1-y2)**2)**.5)


def find_path_length(nme):
    nd=nme
    l=0.0
    while(parent[nd]!=0):
        l=l+direct_len_bet_nodes(nd,parent[nd])
        nd=parent[nd]
    return(l)

def find_n_nearest_node(x,y,n):
    r=1
    while True:
        nearnodes=[]
        for i in list(nodes.keys()):
            if(abs(nodes[i][0]-x)<r and abs(nodes[i][1]-y)<r):
                nearnodes.append(i)
        if(len(nearnodes)==0):
            r+=5
            continue
        ld={}
        for i in nearnodes:
            print('finding nearest')
            ld[i]=(len_bet_points(nodes[i][0],nodes[i][1],x,y))
        sld=list({k: v for k, v in sorted(ld.items(), key=lambda item: item[1])}.keys())
        return(sld[n-1])


def inclination_of_1to2_minuspi_to_pi(x1,y1,x2,y2):
    if(x2-x1==0):
        if(y2>y1):
            return(np.pi/2)
        else:
            return(-np.pi/2)
    else:
        thita=math.atan((y2-y1)/(x2-x1))
        if(x2-x1<0):
            thita=np.pi-thita
        return thita


def obscolchk(x1,y1,x2,y2):
    k=15
    j=0
    while(j<=k):
        x=round(x1+j*(x2-x1)/k)
        y=round(y1+j*(y2-y1)/k)
        j+=1
        if([x,y] in obscontours1):
            print(True)
            return(True)
    return(False)


def descolchk(x1,y1,x2,y2):
    k=15
    j=0
    while(j<=k):
        x=round(x1+j*(x2-x1)/k)
        y=round(y1+j*(y2-y1)/k)
        j+=3
        if([x,y] in dstncontours1):
            print(True)
            return(True)
    return(False)

def do(d,r):                          #d=distance between nodes
    xr=random.randint(0,width)
    yr=random.randint(0,height)
    print('hihi')
    name=find_n_nearest_node(xr,yr,1)
    (xn,yn)=nodes[name]
    thita=inclination_of_1to2_minuspi_to_pi(xn,yn,xr,yr)
    xt=round(xn+d*math.cos(thita))
    yt=round(yn+d*math.sin(thita))
    ptls={}
    nodesnear=[]
    for i in list(nodes.keys()):
        if(len_bet_points(nodes[i][0],nodes[i][1],xt,yt)<=r):
            nodesnear.append(i)
    for i in nodesnear:
        ptls[i]=find_path_length(i)+len_bet_points(nodes[i][0],nodes[i][1],xt,yt)
    ptls={k: v for k, v in sorted(ptls.items(), key=lambda item: item[1])}.keys()
    for i in list(ptls):
        if(obscolchk(nodes[i][0],nodes[i][1],xt,yt)):
            continue
        else:
            if(str(xt)+str(yt) not in list(nodes.keys())):
                create_node(xt,yt,str(xt)+str(yt),i)
                return(str(xt)+str(yt))
    return('nonode')


create_node(59,59,'Start',0)

img2=np.copy(img1)
path=[]

iterations=0


while(True):
    iterations+=1
    print('interation = {}\n-----------------'.format(iterations))
    cnt=do(20,25)
    if(cnt=='nonode'):
        continue
    if(parent[cnt]==0):
        continue
    if descolchk(nodes[cnt][0],nodes[cnt][1],nodes[parent[cnt]][0],nodes[parent[cnt]][1]):
        cnt
        path.append(cnt)
    img2=np.copy(img1)
    print(list(nodes.keys()))
    for i in list(nodes.keys()):
        cv.circle(img2,(nodes[i][0],nodes[i][1]),2,(255,0,255),-1)
        if(parent[i]==0):
            continue
        cv.line(img2,(nodes[i][0],nodes[i][1]),(nodes[parent[i]][0],nodes[parent[i]][1]),color=[0,255,0],thickness=1,lineType=8)
    for i in path:
        pn=i
        while(parent[pn]!=0):
            print('showing path')
            pnp=parent[pn]
            cv.line(img2,(nodes[pn][0],nodes[pn][1]),(nodes[pnp][0],nodes[pnp][1]),color=[255,255,255],thickness=2,lineType=8)
            pn=pnp
    cv.imshow('xd',img2)
    if((len(nodes)%15==0 and len(nodes)<500) or (len(nodes)%100==0 and len(nodes)>500)):
        print('rewiring')
        rewiring(25)
    cv.waitKey(1)
    if(keyboard.is_pressed('s')):
        print('saving--------------------------------------------------------------')
        with open('xdnodes.txt','wb') as fp:
            pickle.dump(nodes,fp,protocol=0)
        with open('xd.txt','wb') as fp1:
            pickle.dump(path,fp1,protocol=0)
        with open('xdparents.txt','wb') as fp2:
            pickle.dump(parent,fp2)
