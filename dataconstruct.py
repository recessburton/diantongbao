#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/7/21 14:51

@author: Gaoxiang Yang, ytc, recessburton@gmail.com
@version: 0.1
"""
import pandas as pd
from pandas import DataFrame
import datainput
import os
import numpy as np

#map first 2 number in ID to province
area = { 11: u"北京", 12: u"天津", 13: u"河北", 14: u"山西",
		 15: u"内蒙古", 21: u"辽宁", 22: u"吉林", 23: u"黑龙江", 31: u"上海",
		 32: u"江苏", 33: u"浙江", 34: u"安徽", 35: u"福建", 36: u"江西",
		 37: u"山东", 41: u"河南", 42: u"湖北", 43: u"湖南", 44: u"广东",
		 45: u"广西", 46: u"海南", 50: u"重庆", 51: u"四川", 52: u"贵州",
		 53: u"云南", 54: u"西藏", 61: u"陕西", 62: u"甘肃", 63: u"青海",
		 64: u"宁夏", 65: u"新疆", 71: u"台湾", 81: u"香港", 82: u"澳门",
		 91: u"国外"
		}

def savetofile(dataframe, filename):
    '''
    save dataframe to .h5 file
    :param dataframe:
    :param filename:
    :return:
    '''
    dataframe.to_hdf(filename, 'df')

def loadfromfile(filename):
    '''
    fetch the DataFrame from .h5 file
    :param filename:
    :return DataFrame:
    '''
    return pd.read_hdf(filename, 'df')

def fetchUserInfo(*filenametuple):
    '''
    get user info. from the specific .xml file(if given filename)
    or the handled datafile(use 'userinfo.h5' as default)
    :param filename:
    :return DataFrame of user info.:
    '''
    if len(filenametuple) == 0:
        return loadfromfile('userinfo.h5')
    filename = filenametuple[0]
    xmlroot = datainput.inputData_xml(filename)
    tags = {'USER_ID':'userid',
            'USER_STATUS':'userstatus',
            'USER_TYPE':'usertype',
            'CERT_NUM':'certnum',
            'INSERT_TIME':'inserttime',
            'BALANCE':'balance'}
    userslist = datainput.getDataByTag_xml(tags, xmlroot)

    for user in userslist:
        #user: a dict element of the list of user-userslist
        if user['certnum'] != "":
            certnum = user['certnum']
            birthdate = certnum[-8:]  # 19780323
            #province = area[int(certnum[:2])]
            province = int(certnum[:2])
            user['birthdate'] = birthdate
            user['province'] = province
        else:
            user['birthdate'] = ""
            user['province'] = np.NaN

    users = DataFrame(userslist)
    #print users
    savetofile(users, 'userinfo.h5')
    return users

def fetchUserAction(*filenametuple):
    '''
    get user action from the specific .xml file(if given filename)
    or the handled datafile(use 'useraction.h5' as default)
    :param filename:
    :return DataFrame of user action:
    '''
    if len(filenametuple) == 0:
        return loadfromfile('useraction.h5')
    # For user action file, we just count the total #log of each user via user_id.
    # That is to say, only user_id column was used to make summation.
    os.system("cat %s |grep user_id| sed 's/[user_id,\/,<,>]//g'| sort| uniq -c > user_id_tmp" % filenametuple[0])
    useraction = pd.read_table('user_id_tmp') #There is a BUG when read from file, the first record, say user_id is 0, is missing. Luckily, the user 0 is superuser.
    os.system("rm user_id_tmp")
    useraction.columns = ['logcount','userid']
    useraction['userid'] = useraction['userid'].astype(str)
    print useraction
    savetofile(useraction,'useraction.h5')
    return useraction

def makeUserData(*userfiles):
    '''
    Construct user data, if userfiles given (tuple), the first element must be
    user info and the second must be user action. If not, it uses the stored file instead.
    :param tuple, userfiles:
    :return DataFrame:
    '''
    if len(userfiles) > 0:
        userinfo = fetchUserInfo(userfiles[0])
        if len(userfiles) > 1:
            useraction = fetchUserAction(userfiles[1])
        else:
            useraction = fetchUserAction()
    else:
        userinfo = fetchUserInfo()
        useraction = fetchUserAction()
    userdata = pd.merge(userinfo, useraction, on='userid', how='left')
    #userdata.to_csv('userdata.csv', encoding='gbk')
    return userdata

if __name__ == '__main__':
    filename = 't_user_action_log.xml'
    useraction= fetchUserAction()
    userinfo = fetchUserInfo()
    userdata = pd.merge(userinfo, useraction, on = 'userid', how = 'left')
    userdata['logcount'] = userdata['logcount'].fillna(1)
    print userdata
