#!/usr/bin/python
import json
import urllib2
from pprint import pprint


def jsonConnection(operatingSystem):
    ec2_os_names_translation = {
    "linux" : "linux",
    "rhel" : "rhel",
    "sles" : "sles",
    "windows" : "mswin",
    "none" : "linux"
    }
    
    InstanceTypeJsonConnection = {
    "linux" : "http://aws.amazon.com/ec2/pricing/json/linux-od.json",
    "rhel" : "http://aws.amazon.com/ec2/pricing/json/rhel-od.json",
    "sles" : "http://aws.amazon.com/ec2/pricing/json/sles-od.json",
    "mswin" : "http://aws.amazon.com/ec2/pricing/json/mswin-od.json",
    "mswinSQL" : "http://aws.amazon.com/ec2/pricing/json/mswinSQL-od.json",
    "mswinSQLWeb" : "http://aws.amazon.com/ec2/pricing/json/mswinSQLWeb-od.json",
    }
    translatedOsName = ec2_os_names_translation[operatingSystem]
    JsonURL = InstanceTypeJsonConnection[translatedOsName]
#    print JsonURL
    response = urllib2.urlopen(JsonURL)
    awsjson = response.read()
    aws_data = json.loads(awsjson)
#    print aws_data
    return aws_data

def OSDecoder(operatingSystem):
    ec2_os_names_translation = {
    "linux" : "linux",
    "rhel" : "rhel",
    "sles" : "sles",
    "windows" : "mswin",
    "none" : "linux"
    }
    OsName = ec2_os_names_translation[operatingSystem]
    return OsName

def regionDecoder(providedRegion):
    EC2_REGIONS_API_TO_JASON_NAME = {
        "us-east" : "us-east",
        "us-east-1" : "us-east",
        "us-west-2" : "us-west-2", 
        "us-west-1" : "us-west",
        "eu-west-1" : "eu-ireland",
        "ap-southeast-1" : "apac-sin",
        "ap-southeast-2" : "apac-syd",
        "apac-syd" : "apac-syd",
        "ap-northeast-1" : "apac-tokyo",
        "sa-east-1" : "sa-east-1"
}
    jsonRegionName = EC2_REGIONS_API_TO_JASON_NAME[providedRegion]
    return jsonRegionName   

def instanceOS(os):
    DISPLAY_NAME_TO_JASON_NAME = {
        "Ubuntu" : "linux",
        "RHEL" : "rhel",
        "SLES" : "sles",
        "Centos" : "linux",
        "windows" : "windows",
        "Linux" : "linux",
        "linux" : "linux"
    }
 
    running_OS = DISPLAY_NAME_TO_JASON_NAME[os]
    return running_OS
  
  
def INSTANCE_SIZE_MAPPING(EncodedInstanceSize):
    encodInstanceSize = EncodedInstanceSize.split(".")[1]
    INSTANCE_SIZE_MAPPING = {   
        "micro" :"u" ,
        "small":"sm" ,
        "medium":"med" ,
        "large": "lg",
        "xlarge":"xl",
        "2xlarge":"xxl" ,
        "4xlarge": "xxxxl" ,
        "8xlarge": "xxxxxxxxl"
    }
    decodeInstanceSize = INSTANCE_SIZE_MAPPING [encodInstanceSize]  
    return decodeInstanceSize


def INSTANCE_TYPE_MAPPING(EncodedServerType):
    ServerSize = EncodedServerType
    encodedInstanceType = ServerSize.split(".")[0]
    encodeDecodeList = {"m1" : "stdODI",
                        "t1" : "uODI",
                        "m2" : "hiMemODI",
                        "c1" : "hiCPUODI" ,
                        "cc1": "clusterComputeI",
                        "cg1": "clusterGPUI",
                        "hi1": "hiIoODI",
                        "m3" : "secgenstdODI",
                        "hs1": "hiStoreODI",
                        "cr1": "clusterHiMemODI"
                        }
    decodedInstanceType = encodeDecodeList[encodedInstanceType]
    return decodedInstanceType
    
	
def getCostPerHour(regionToCost, platform ,serverSize):
    ServerCost = 0
    AWS_DATA=jsonConnection(platform)	
    for regions in AWS_DATA['config']['regions']:
        regionName = regions['region']
        decodedRegionToCost = regionDecoder(regionToCost)
        if (regionName == decodedRegionToCost): #Checking for there region
            #print regionName
            for instanceTypes in regions['instanceTypes']:
                instanceType = instanceTypes['type']
#                decodedInstanceType = INSTANCE_TYPE_MAPPING(serverSize)
                #decodedInstanceType = serverSize
#                print "instance type: " + instanceType
                #if (decodedInstanceType == instanceType):
                for sizes in instanceTypes['sizes']:
                     decodedInstanceSize = INSTANCE_SIZE_MAPPING(serverSize)
                         #
                     decodedInstanceSize = serverSize
                     size = sizes['size']
#                     print "size: " + size
                         #if (decodedInstanceSize == size):
                     if (serverSize == size):
                             #print "decoded size: " + decodedInstanceSize
                         for valueColumns in sizes['valueColumns']:
                             OSTypeName = valueColumns['name']
                             platformOSName = OSDecoder(platform)
                             if (OSTypeName == platformOSName):
                                 ServerCost = valueColumns['prices']['USD']


    return ServerCost
	
#def main ():
#  serverCostSS = getCostPerHour("us-east-1","linux","c3.xlarge")
#   print serverCostSS
#if __name__ == "__main__":
#    main()
