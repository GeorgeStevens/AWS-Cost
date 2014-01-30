#!/usr/bin/python
import boto
from boto.s3.connection import S3Connection
from boto.s3.connection import OrdinaryCallingFormat
from datetime import datetime
from prettytable import PrettyTable
import JsonParser
import CostCalculation
import sys
import yaml
#import Database

file2write = open("RunningServerList.txt","w")
costForAccount=0

def get_connection(accessKey,secretKey):
    conn = boto.connect_ec2(accessKey,secretKey)

def get_region_connection(regionName,accessKey,secretKey):
    conn = boto.connect_ec2(accessKey,secretKey)
    if (regionName != ""):
        regionConnection = boto.ec2.connect_to_region(regionName,aws_access_key_id=accessKey,aws_secret_access_key=secretKey)
    return regionConnection

def get_storage_connection(accessKey,secretKey):    
    storageConn = S3Connection(accessKey,secretKey)
    return storageConn
        
    
    
def Storage(accessKey,storageKey):
    # Storge bucket
    storageConn = get_storage_connection(accessKey,storageKey)

    storageTable = PrettyTable (["Storage Buckets", "Total Size"])
    storageTable.align["Storage Buckets"] = "l"
    storageTable.padding_width = 1
    

    boto.connect_s3(calling_format=OrdinaryCallingFormat())
    reservationStorage = storageConn.get_all_buckets()
    totalSize = 0

    for bucket in reservationStorage:
        s3Bucket = bucket.name
        if (bucket.name != 'esbundles-c14334.Ubuntu-1204-PE-300-agent'):           
            for key in bucket.list():
                size = key.size
                totalSize = totalSize + size
        storageTable.add_row([s3Bucket,""])        
    #print 'TotalSize: ' + str(totalSize/1073741824) + ' GB'
    totalSize = totalSize/1073741824
    storageTable.add_row(["---------------------------------------------------", "------------"])
    storageTable.add_row(["Total Size in GB", totalSize])
    print storageTable
    file2write.writelines('\n')
    file2write.writelines(str(storageTable))
    
    
def timeRunning(timepar):
    time = timepar
    cleanedTime = time.replace ('.000Z', '')
    startDateTime = cleanedTime.replace ('T',' ')   
    serverStartDateTime = datetime.strptime(startDateTime, '%Y-%m-%d %H:%M:%S')
    currentDateTime = datetime.now()
    elapsedTime = currentDateTime - serverStartDateTime
    elapsedHours = abs(elapsedTime).total_seconds() / 3600.0
    return int(elapsedHours)
    
def instanceImagesOS(region, imageID, accessKey,secretKey):
    regionConnection = get_region_connection(region,accessKey,secretKey)
    images = regionConnection.get_all_images(imageID)
    ubuntu = "ubuntu"
    rhel = "RHEL"
    sles = "SLES"
    centos ="centos"
#    print images
    for image in images:
        imageName = str(image.name)
        imagePlatform = str(image.platform)
        if (imagePlatform == "None"):
            if (ubuntu.lower() in imageName.lower()):
                operatingSystem = "Ubuntu"
                return operatingSystem
            elif (rhel.lower() in imageName.lower()):
                operatingSystem = "RHEL"
                return operatingSystem
            elif (sles.lower() in imageName.lower()):
                operatingSystem = "SLES"
                return operatingSystem
            elif (centos.lower() in imageName.lower()):
                operatingSystem = "CentOS"
                return operatingSystem
            else:
                operatingSystem = "linux"
                return operatingSystem
    return "Linux"

def CreatPdf():
     runningServersPdf.set_author('George Stevens')
     runningServersPdf.set_title("List of running serevrs for AWS")
     filename = str(file2write)

     runningServersPdf.print_chapter(1,'Running Servers','RunningServerList.pdf')
    
def Servers(accessKey,secretKey):
    totalAccountCost = 0
    # Generate list of servers  
    for region in boto.ec2.regions():
        if region.name != 'us-gov-west-1':            

            regionConnection = get_region_connection(region.name,accessKey,secretKey)
            reservations = regionConnection.get_all_instances()
#            print ('\n')
#            print('Region: ' + str(regionConnection).replace("EC2Connection:ec2.","") )
#
#            file2write.writelines('\n')
#            file2write.writelines('Region: ' + str(regionConnection).replace("EC2Connection:ec2.",""))
#            file2write.writelines('\n')
            
            serverTable = PrettyTable (["Server Name", "Owner/Creator","InstanceType","LaunchTime","Hours Running","Cost/Hour","Running Cost","Architecture","OS","ID","Public_dns_name","IP","State","Label"])
            serverTable = PrettyTable (["Server Name", "Owner/Creator","InstanceType","Launch Date","Cost/Hour","Running Cost"])
            serverTable.align["Server Name"] = "l"
            serverTable.padding_width = 1
            regionCost = 0
            itemCount = 0
            
            if reservations:
                #print reservations
                for reservation in reservations:
                    instance = reservation.instances
                    for instDetails in instance:
                        serverState = str(instDetails.__dict__['_state'])
                        if (serverState != 'stopped(80)' and serverState != 'terminated(48)'):
                            serverName = str(instDetails.__dict__['tags']['Name'])
                            ownerCreator = str(instDetails.__dict__['tags']['es:Owner'])
                            instanceType = str(instDetails.__dict__['instance_type'])
                            launchTime = (str(instDetails.__dict__['launch_time']).replace('T',' ')).replace ('.000Z','')
                            runningTime = str(timeRunning(launchTime))
                            imageID = str(instDetails.__dict__['image_id'])
                            architecture =  str(instDetails.__dict__['architecture'])
                            OS = str(instDetails.__dict__['platform'])
                            if (OS == "None"):
                                OS = str(instanceImagesOS(region.name,imageID,accessKey,secretKey))
#                                osOfInstance = str(instanceOS(region.name,imageID))
                            ID = str(instDetails.__dict__['id'])
                            public_dns_name = str(instDetails.__dict__['public_dns_name'])
                            IP = str(instDetails.__dict__['ip_address'])
                            state = str(instDetails.__dict__['_state']).replace('(16)','')
                            label = str(instDetails.__dict__['tags']['es:Label'])
                            regionForCosting = str(region.name)
                            running_OS = JsonParser.instanceOS(OS)
                            regionToCosting = JsonParser.regionDecoder(regionForCosting)
                            costPerHour = JsonParser.getCostPerHour(regionToCosting,running_OS.lower(),(instanceType.lower()))
                            totalRunningCost = CostCalculation.CostCalulation(int(runningTime),costPerHour)
#                            serverTable.add_row([serverName,ownerCreator,instanceType,launchTime,runningTime,costPerHour,totalRunningCost,architecture,OS,ID,public_dns_name,IP,state,label])
                            serverTable.add_row([serverName,ownerCreator,instanceType,launchTime,costPerHour,round(totalRunningCost,2)])
                            regionCost = regionCost + totalRunningCost
                            itemCount = itemCount + 1
                            #accountCost(regionCost)
#            print itemCount
            if (itemCount > 0):
                print ('\n')
                print('Region: ' + str(regionConnection).replace("EC2Connection:ec2.","") )

                file2write.writelines('\n')
                file2write.writelines('Region: ' + str(regionConnection).replace("EC2Connection:ec2.",""))
                file2write.writelines('\n')
                print serverTable
                print "Cost for region "+ str(regionConnection).replace("EC2Connection:ec2.","") + ": $" + str(round(regionCost,2))
                file2write.writelines(str(serverTable))
                file2write.writelines('\n')
                file2write.writelines("Cost for region " + str(regionConnection).replace("EC2Connection:ec2.","") + ": $" + str(round(regionCost,2)))
                file2write.writelines('\n')
            #file2write.close()
            #print "Account Cost: " + str(totalAccountCost)
            totalAccountCost = totalAccountCost + regionCost
            #print "TotalAccountCost: " + str(totalAccountCost)
    return totalAccountCost

def accountCost(cost):
    totalCost = totalCost + cost

def main(accounts_file):
    totalAccountCost = 0

    f=open(accounts_file)
    parsed=yaml.safe_load(f)
#    print parsed

    for key,value in parsed.iteritems():
        account_name=key
        account_number=value['account_number']
        access_key=value['access_key']
        secret_key=value['secret_key']
    #for accountName in Database.listAllAccounts():
        print key
        #print accountName[0]
        file2write.writelines('---------------------------------------------------------------------------------------\n\n')
        file2write.writelines("Account Name: " + account_name)
        file2write.writelines('\n\n')
        get_connection(access_key,secret_key)
        totalAccountCost = Servers(access_key,secret_key)
        print "Total cost for account: " + str(round(totalAccountCost,2))
        file2write.writelines('\n')
        file2write.writelines("Total cost for the Account : $" + str(round(totalAccountCost,2)))
        file2write.writelines('\n')
        totalAcccountCost = 0
#        print "TotalAccountCost in for loop: " + str(totalAccountCost)

#    
if __name__ == "__main__":
    main(sys.argv[1])
