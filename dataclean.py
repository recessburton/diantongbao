#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/7/22 13:33

@author: Gaoxiang Yang, ytc, recessburton@gmail.com
@version: 0.1
"""

import dataconstruct

def dataClean(userdata):
    userdata['logcount'] = userdata['logcount'].fillna(1)