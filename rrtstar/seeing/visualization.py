import pickle
import time
import numpy as np
import cv2 as cv
img=cv.imread('1.png')

dstn=[0,255,0]
path=[]
dstnx,dstny=np.where(np.all(img==dstn,axis=2))
dstncrdnts=list(np.column_stack((dstny,dstnx)))
dstncrdnts=[list(i) for i in dstncrdnts]
print(dstncrdnts)

with open('xdnodes.txt','rb') as fp:
    nodes=(pickle.load(fp))
with open('xdparents.txt','rb') as fp:
    parents=(pickle.load(fp))

nodenames=list(nodes.keys())
for i in nodenames:
    if(parents[i]==0):
        continue
    cv.circle(img,(nodes[i][0],nodes[i][1]),2,(255,0,255),-1)
    cv.line(img, (nodes[i][0],nodes[i][1]),(nodes[parents[i]][0],nodes[parents[i]][1]), (0, 255, 0), thickness=1, lineType=8)
    cv.imshow('xd',img)
    cv.waitKey(1)
for i in nodenames:
    if(parents[i]==0):
        continue
    if[nodes[i][0],nodes[i][1]] in dstncrdnts:
        path.append(i)
print(path)
for i in path:
        pn=i
        print('for')
        while(parents[pn]!=0):
            print('showing path')
            pnp=parents[pn]
            cv.line(img,(nodes[pn][0],nodes[pn][1]),(nodes[pnp][0],nodes[pnp][1]),color=[255,255,255],thickness=2,lineType=8)
            pn=pnp
            cv.imshow('xd',img)
            cv.waitKey(10)
cv.waitKey(0)
