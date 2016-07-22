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

k = 5  # #cluster
cpus = 2 # #cup kernels

userinfofilename = 't_user_origin.xml'
userdata = dataconstruct.fetchUserInfo(userinfofilename)


kmodel = KMeans(n_clusters = k, n_jobs = 2)
kmodel.fit(userdata) #train data

kmodel.cluster_centers_ #show cluster center
kmodel.labels_ #show class of sample
