#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/7/22 13:33

@author: Gaoxiang Yang, ytc, recessburton@gmail.com
@version: 0.1
"""

import pandas as pd
import dataconstruct

def birthdateToYear(birthdatestr):
    '''
    Use an int to stand for birthyear decades
    birthyear->int, e.g. 5,6,7,8,9,10 stand for 50s,60s,70s,80s,90s,00s respectively.0 stands for None .
    :param birthdatestr:
    :return int:
    '''
    if len(birthdatestr) == 0:
        return 0
    else:
        if int(birthdatestr) > 20100000 or int(birthdatestr) < 19200000:
            return 0
        birthyear = int(birthdatestr[:4])
    return (birthyear - 1900) / 10


def dataClean(userdata):
    userdata['logcount'] = userdata['logcount'].fillna(1)
    userdata = userdata.drop('certnum', axis = 1)
    userdata = userdata.drop('inserttime', axis = 1)
    userdata = userdata.drop('userid',axis = 1)
    userdata['birthdate'] = userdata['birthdate'].apply(birthdateToYear)
    userdata['logcount'] = userdata['logcount'].fillna(1)
    userdata['province'] = userdata['province'].fillna(0)
    #userdata['balance'] = userdata['balance'].astype(float) #dataframe cannot convert string to float
    userdata['balance'] = pd.to_numeric(userdata['balance'], errors='coerce')
    userdata['userstatus'] = userdata['userstatus'].astype(int)
    userdata['usertype'] = userdata['usertype'].astype(int)
    userdata.to_csv('userdata.csv', encoding='gbk', index=False)
    return userdata

if __name__ == '__main__':
    userdata = dataconstruct.makeUserData()
    dataClean(userdata)