#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/7/25 08:52

@author: Gaoxiang Yang, ytc, recessburton@gmail.com
@version: 0.1
"""

def kmeansPretreatment(userdata):
    '''
    Drop some unused columns in userdata
    :param userdata:
    :return DataFrame:
    '''
    userdata = userdata.drop('birthdate', axis=1)
    userdata = userdata.drop('province', axis=1)
    userdata = userdata.drop('userstatus', axis=1)
    userdata = userdata.drop('usertype', axis=1)
    kmeanscleaneddata = userdata

    return kmeanscleaneddata

def kmeansStandardize(kmeanscleaneddata):
    '''
    Standardize the cleaned data for kmeans
    :param kmeanscleaneddata:
    :return DataFrame:
    '''
    kmeansStandardizedData = (kmeanscleaneddata - kmeanscleaneddata.mean()) / (kmeanscleaneddata.std())
    kmeansStandardizedData.to_csv('kmeansStandardizedData.csv', encoding='gbk', index=False)
    return kmeansStandardizedData