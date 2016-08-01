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

def fetchUserInfo(filenamelist):
    '''
    get user info. from the specific .xml file(if given filename)
    or the handled datafile(use 'userinfo.h5' as default)
    :param filename:
    :return DataFrame of user info.:
    '''
    if len(filenamelist) == 0 or filenamelist[0] == "":
        print "User Info: use saved file."
        return loadfromfile('userinfo.h5')
    filename = filenamelist[0]
    print "User Info: filename"
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

def fetchUserAction(filenamelist):
    '''
    get user action from the specific .xml file(if given filename)
    or the handled datafile(use 'useraction.h5' as default)
    :param filename:
    :return DataFrame of user action:
    '''
    if len(filenamelist) == 0:
        print "User Action Data: use saved file."
        return loadfromfile('useraction.h5')
    # For user action file, we just count the total #log of each user via user_id.
    # That is to say, only user_id column was used to make summation.
    print "User Action Data:", filenamelist
    for file in filenamelist:
        os.system("cat %s |grep user_id| sed 's/[user_id,\/,<,>]//g'>> user_id_tmp" % file)

    os.system("sort user_id_tmp | uniq -c > user_id_tmp_combined")
    useraction = pd.read_table('user_id_tmp_combined') #There is a BUG when read from file, the first record, say user_id is 0, is missing. Luckily, the user 0 is superuser.
    os.system("rm user_id_tmp user_id_tmp_combined")
    useraction.columns = ['logcount','userid']
    useraction['userid'] = useraction['userid'].astype(str)

    savetofile(useraction,'useraction.h5')
    return useraction

def makeUserData(userdata, useraction):
    '''
    Construct user data, the userdata and useraction is LIST type of filenames
    :param lists:
    :return DataFrame:
    '''
    userinfo = fetchUserInfo(userdata)
    useraction = fetchUserAction(useraction)
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
