#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/7/21 10:06

@author: ytc recessburton@gmail.com
@version: 0.1
"""

import xml.dom.minidom as xmlm
import xml.parsers.expat
import os

###################################################################
# XML file input
###################################################################
'''
In this scenario, the given XML file looks like bellow:
<RECORDS>
    <RECORD>
        <USER_ID>419</USER_ID>
        <USER_NAME>P008001</USER_NAME>
        <USER_STATUS>0</USER_STATUS>
        <USER_TYPE>1</USER_TYPE>
        <SEX>0</SEX>
        <CERT_NUM>21070219670520</CERT_NUM>
        <INSERT_TIME>04/18/2016 10:34:11</INSERT_TIME>
        <BALANCE>0</BALANCE>
        <DEL_FLAG>0</DEL_FLAG>
        <DISABLE>0</DISABLE>
        <NICK_NAME>点通宝会员</NICK_NAME>
    </RECORD>
    <RECORD>
    ...
    </RECORD>
    ...
</RECORDS>
The XML is exported from the database by default config. which means
every RECORD has only one layer of children,columns of table, which
has no subsequent offsprings.
'''

def inputData_xml(filepath):
    '''
    Open the xml file and return the full doc's element structure.
    WARNINGS: THIS FUNCTION WOULD FAIL FOR INVALID TOKEN IN VALUE
    LIKE UNREADABLE LETTER SUCH AS ^A, ^T. THAT MEANS YOU MUST REMOVE
    THEM FIRST SOMETIMES BY HAND.
    :param filepath:
    :return xml.dom.minidom.Element:
    '''
    hasexception = True
    for i in range(2):
        if hasexception == False:
            break
        try:
            dom = xmlm.parse(filepath)
            hasexception = False
        except xml.parsers.expat.ExpatError, e:
            print e
            #In MAC OS X system, the sed is modified.
            #Use parameter '-i.bak' instead of '-i'.
            #The unprintable characters such like ^A are always occurs
            #in USER_NAME or NICK_NAME tag.
            os.system("sed -i.bak 's/NAME>[\x01-\x1F]/NAME>/g' %s" % (filepath))
            os.system("rm %s.bak" % (filepath)) #ONLY IN MAC
    return dom.documentElement

def getDataByTag_xml(tags, xmlroot):
    '''
    Return the list of values (of any __class__) between compared tags
    as rows of given columns in a table.
    :param tagname:
    :param xmlroot:
    :return list of values between given tag:
    '''
    users = []
    records = xmlroot.getElementsByTagName('RECORD')
    for record in records:
        user = {}
        for tag in tags.keys():
            elementwithvalue = record.getElementsByTagName(tag)
            try:
                user[tags[tag]] = elementwithvalue[0].firstChild.data
            except:
                user[tags[tag]] = ""
        users.append(user)
    return users

if __name__ == '__main__':
    filepath = 't_user_origin.xml'
    inputData_xml(filepath)
'''
try:
    user[tags[tag]] = elementwithvalue.frstChild.data
except AttributeError, e:
    user[tags[tag]] = ""
    print user
finally:
    users.append(user)
'''