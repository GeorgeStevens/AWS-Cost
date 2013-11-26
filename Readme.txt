AccountCostCalculator
=====================

AWS pricing tool was developed to check he cost of the servers running in a account

Installaiton
============
In order to get the calcualtor working and runnin on your system teh vollowing needs to be performed
1. Install the following pyhton modules with pip or easyinstall
	boto
	datetime
	prettytable
	json
	urllib2
	sqlite3
	pprint
2. Polulate/Create a sqlite3 database by adding the required credentials to the createDatabase method in the file Database.py.
   Uncoment the createDatabase method call in the main method and execute the file with python Database.py This will create a 
   datbase with the name credentialsDB.db
   Alternatively, check out the yaml brance. 
   Create a yaml file with the account details you want to use and run it in the following manner:
   python AccountCoastCalculator.py accounts.yaml 
3. Execute the file AccountCoastCalculator.py with python AccountCoastCalculator.py 
4. A list of runnign server in the regons will be printed out on screen and a File named RunningServerList.txt will also be
   created with this list.
   Example out put 
   ========================================================================================================================
   ---------------------------------------------------------------------------------------

  Account Name: CSE


  Region: us-west-2.amazonaws.com
  +------------------------------------------------------------+----------------+--------------+---------------------+-----------+--------------+
  | Server Name                                                | Owner/Creator  | InstanceType |     Launch Date     | Cost/Hour | Running Cost |
  +------------------------------------------------------------+----------------+--------------+---------------------+-----------+--------------+
  | pairing01                                                  | Owner          |   m1.small   | 2013-04-03 20:54:04 |   0.060   |    294.66    |
  | infa--git                                                  | Owner          |   m1.large   | 2013-07-15 02:55:19 |   0.240   |    589.68    |
  | Service-tier-independent-node-0-(replacement-2013821-1726) | Owner          |   m1.small   | 2013-08-21 17:26:34 |   0.060   |     93.3     |
  | XX-idrac-box                                               | Owner          |  m1.medium   | 2013-10-09 06:31:16 |   0.182   |    70.98     |
  | Puppet Agent Install                                       | Owner          |   m1.small   | 2013-09-30 15:27:50 |   0.120   |    71.64     |
  | redhat-mirror                                              | Owner          |  m1.medium   | 2013-09-25 04:26:17 |   0.170   |    123.76    |
  +------------------------------------------------------------+----------------+--------------+---------------------+-----------+--------------+
  Cost for region us-west-2.amazonaws.com: $1244.02

  Region: us-east-1.amazonaws.com
  +-----------------------+------------------+--------------+---------------------+-----------+--------------+
  | Server Name           |  Owner/Creator   | InstanceType |     Launch Date     | Cost/Hour | Running Cost |
  +-----------------------+------------------+--------------+---------------------+-----------+--------------+
  | demo-222              | Owner            |   m1.small   | 2013-07-22 18:32:17 |   0.060   |    136.44    |
  | SM-SQLSlave           | Owner            |   m1.small   | 2013-08-07 14:19:37 |   0.060   |    113.64    |
  | XXXXX_ADTest          | Owner            |   m1.small   | 2013-06-19 19:13:44 |   0.060   |    183.9     |
  | sdsd                  | Owner  	     |  m1.xlarge   | 2013-08-22 22:55:26 |   0.480   |    732.0     |
  | pe-30-web3            | Owner  	     |   m1.small   | 2013-08-20 23:41:52 |   0.060   |    94.38     |
  | SM-SQLMaster          | Owner            |   m1.small   | 2013-08-07 14:19:07 |   0.060   |    113.64    |
  | Demo-GSA              | Owner            |  m1.xlarge   | 2013-10-08 16:12:21 |   0.480   |    193.92    |
  | XXXXXXXX-win2003-64-1 | Owner            |   m1.small   | 2013-10-23 20:10:44 |   0.091   |     3.64     |
  | XXXXXXXX-win2003-86-1 | Owner            |   m1.small   | 2013-10-23 20:09:56 |   0.091   |     3.64     |
  | XXXXhel62-i2-2        | Owner            |   m1.large   | 2013-10-22 15:46:52 |   0.300   |     20.4     |
  | XXXAD2                | Owner            |   m1.large   | 2013-04-02 15:36:56 |   0.364   |   1798.52    |
  | XXXrhel62-2           | Owner            |  m1.medium   | 2013-10-03 16:01:42 |   0.120   |    62.88     |
  | Demo-AD               | Owner            |   m1.small   | 2013-04-26 14:46:50 |   0.091   |    397.21    |
  +-----------------------+------------------+--------------+---------------------+-----------+--------------+
  Cost for region us-east-1.amazonaws.com: $3854.22

  Total cost for the Account : $5098.24

 
  
