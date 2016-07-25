#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/7/20 10:19

@author: ytc recessburton@gmail.com
@version: 0.1
"""

import pandas as pd
from sklearn.cluster import KMeans
import dataconstruct
import dataclean
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from pandas import Series
import kmeanspretreatment

k = 5  # #cluster
cpus = 2 # #cup kernels

#map first 2 number in ID to province
area = { 0:u"未知", 11: u"北京", 12: u"天津", 13: u"河北", 14: u"山西",
		 15: u"内蒙古", 21: u"辽宁", 22: u"吉林", 23: u"黑龙江", 31: u"上海",
		 32: u"江苏", 33: u"浙江", 34: u"安徽", 35: u"福建", 36: u"江西",
		 37: u"山东", 41: u"河南", 42: u"湖北", 43: u"湖南", 44: u"广东",
		 45: u"广西", 46: u"海南", 50: u"重庆", 51: u"四川", 52: u"贵州",
		 53: u"云南", 54: u"西藏", 61: u"陕西", 62: u"甘肃", 63: u"青海",
		 64: u"宁夏", 65: u"新疆", 71: u"台湾", 81: u"香港", 82: u"澳门",
		 91: u"国外"
		}

classlabels = { 0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I'}

userinfofilename = 't_user_origin.xml'
userdata = dataconstruct.makeUserData()
usercleaneddata = dataclean.dataClean(userdata)
kmeansdata = kmeanspretreatment.kmeansPretreatment(usercleaneddata)
kmeansdata = kmeanspretreatment.kmeansStandardize(kmeansdata)
classifydatafile = 'kmeansStandardizedData.csv'

classifydata = pd.read_csv(classifydatafile)

kmodel = KMeans(n_clusters = k, n_jobs = 2)
kmodel.fit(classifydata) #train data

print kmodel.cluster_centers_ #show cluster center
print kmodel.labels_ #show class of sample

classifydata['class'] = Series(classlabels[i] for i in kmodel.labels_)
outputdata = DataFrame(classifydata)
outputdata['province']= Series([area[int(i)] for i in usercleaneddata['province'].values])
outputdata['birthdate'] = userdata['birthdate']
outputdata['balance'] = usercleaneddata['balance']
outputdata['logcount'] = usercleaneddata['logcount']
outputdata['usertype'] = userdata['usertype']
outputdata['userstatus'] = userdata['userstatus']
outputdata['userid'] = userdata['userid']

outputdata.to_csv('class_1.csv', encoding='utf-8')

print "Classification Completed."
