# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 20:00:23 2017

@author: Administrator
"""

import pandas as pd

inputfile = 'data/评论'
outputfile = 'data/pos.xls'
outputfile1 = 'data/neg.xls'
newdata=pd.DataFrame()
newdata1=pd.DataFrame()
num=10
for i in range(num):
    #print(i)
    data = pd.read_excel(inputfile+str(i)+'.xls')
    ndata=data[u'评价'][(data[u'口味']>3)&(data[u'环境']>3)&(data[u'服务']>3)]
    #newdata.append(ndata,ignore_index=True)
    newdata=pd.concat([newdata,ndata])
    # data[u'评价'][(int(data[u'口味'])>3|int(data[u'环境'])>3|int(data[u'服务'])>3)]
newdata.to_excel(outputfile,header=False,index=False)

for i in range(num):
    #print(i)
    data1 = pd.read_excel(inputfile+str(i)+'.xls')
    ndata1=data1[u'评价'][(data1[u'口味']<3)&(data1[u'环境']<3)&(data1[u'服务']<3)]
    #newdata.append(ndata,ignore_index=True)
    newdata1=pd.concat([newdata1,ndata1])
    # data[u'评价'][(int(data[u'口味'])>3|int(data[u'环境'])>3|int(data[u'服务'])>3)]
newdata1.to_excel(outputfile1,header=False,index=False)