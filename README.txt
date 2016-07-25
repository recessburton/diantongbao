Copyright (C),2014-2016, YTC, BJFU, www.bjfulinux.cn, www.muheda.com
Created on 16/7/20 10:19

@author: Gaoxiang Yang, ytc, recessburton@gmail.com
@version: 0.1

This application targets to classify the users in Diantongbao app.

User info table and user action table are taken into consideration.
In user info table we consider the following features:
balance: specifies current points of user
birthdate: specifies chronological decades of user’s birthdate
province:
userstatus:
usertype:
While in kmeans classification process, we only exploit the standardized
balance column, which is a continuous value.

In user action table however, we only utilize the userid info actually which
specified as logcount.
logcount: specifies the summation of logs each time the user operates on app. 
It’s the count of each userid in user action table.

In all, we have TWO columns in kmeans classifying process.

The result file is name as class.csv in this application path.
The class column stands for the types of each user which varies from A-E.
