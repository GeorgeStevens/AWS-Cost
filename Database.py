# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:59:22 2013

@author: gstevens
"""

import sqlite3

def createDatabase():
    dbConnection = sqlite3.connect('credentialsDB.db')

    credConnection = dbConnection.cursor()
    credConnection.execute('''CREATE TABLE credentials (accountName text, accessKey text, secretKey text)''')
    credConnection.execute("INSERT INTO credentials VALUES ('ACCOUNTNAME_HERE','ACCESSKEY_HERE','SECRETKEY_HERE')")
    credConnection.execute("INSERT INTO credentials VALUES ('ACCOUNTNAME_HERE','ACCESSKEY_HERE','SECRETKEY_HERE')")
    
    dbConnection.commit()
    credConnection.close()
    print "Finished creating the database, Please remember to comment the main method again"
    
def connectToDB():
    dbConnection = sqlite3.connect('credentialsDB.db')
    credConnection = dbConnection.cursor()
    return credConnection
    
def listAllAccounts():
    
    credConnection = connectToDB()
    records = credConnection.execute ('select accountName from credentials')
    return records

    
def getAccountAccessKey(accName):
    credConnection = connectToDB()
    accountName = (accName,)
    credConnection.execute ('select accessKey from credentials where accountName=?',accountName)
    accessKey = credConnection.fetchone()
    return accessKey
    
def getAccountAccessSecretKey(accName):
    credConnection = connectToDB()
    accountName = (accName,)
    credConnection.execute ('select secretKey from credentials where accountName=?',accountName)
    secretKey =  credConnection.fetchone()
    return secretKey
    
   
def main ():
#   createDatabase()
if __name__ == "__main__":
    main()
