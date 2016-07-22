#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/7/21 14:51

@author: ytc recessburton@gmail.com
@version: 0.1
"""

from pandas import DataFrame
from pandas import Series
import datainput

#map first 2 number in ID to province
area = { 11: "北京", 12: "天津", 13: "河北", 14: "山西",
		 15: "内蒙古", 21: "辽宁", 22: "吉林", 23: "黑龙江", 31: "上海",
		 32: "江苏", 33: "浙江", 34: "安徽", 35: "福建", 36: "江西",
		 37: "山东", 41: "河南", 42: "湖北", 43: "湖南", 44: "广东",
		 45: "广西", 46: "海南", 50: "重庆", 51: "四川", 52: "贵州",
		 53: "云南", 54: "西藏", 61: "陕西", 62: "甘肃", 63: "青海",
		 64: "宁夏", 65: "新疆", 71: "台湾", 81: "香港", 82: "澳门",
		 91: "国外"
		}

def fetchUserInfo(filename):
    '''
    get user info. from the specific .xml file
    :param filename:
    :return DataFrame of user info.:
    '''
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
            province = area[int(certnum[:2])]
            user['birthdate'] = birthdate
            user['province'] = province
        else:
            user['birthdate'] = ""
            user['province'] = ""

    users = DataFrame(userslist)
    #print users
    return users

def fetchUserAction(filename):
    '''
    get user action from the specific .xml file
    :param filename:
    :return DataFrame of user action:
    '''
    return useraction

if __name__ == '__main__':
    filename = 't_user_origin.xml'
    fetchUserInfo(filename)