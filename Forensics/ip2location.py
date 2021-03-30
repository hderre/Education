#!/usr/bin/env python3

# Title: Ip location lookup tool
# Version: 0.1 
# Date: March 2021
# Author: Hendrik Derre
# Description: This tool will lookup all the IP addresses in a file on ipinfo.io and return ip, country, region and org. For educational purposes only!

import argparse, sys, os.path
from urllib.request import urlopen
from json import load

def ipInfo(addr=''):
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        if Token == "":
            url = 'https://ipinfo.io/' + addr + '/?token='
        else:
            url = 'https://ipinfo.io/' + addr + '/?token=' + Token
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = load(res)
    line = (str(data.get('ip'))+";"+str(data.get('country'))+";"+str(data.get('region'))+";"+str(data.get('org')))
    return str(line)
       
#Menu
parser = argparse.ArgumentParser(description='IP lookup Tool - Forensics')
parser.add_argument("-f", action="store", dest="addr_file", required=True, help="File with list of IPs to lookup (one ip per line)")
parser.add_argument("-o", action="store", dest="output_file", default="output.csv", required=False, help="output csv file")
parser.add_argument("-t", action="store", dest="token", default="", required=False, help="ipinfo.io token")
args = parser.parse_args()

#get token from https://ipinfo.io/account/home
Token = args.token

# initialize the addr_file object
if(os.path.isfile(args.addr_file)):
    filename = args.addr_file
else:
    print("[!] Error: file does not exist")
    exit(0)  

#create new file (write)
out = open(args.output_file,"w")

#read file and lookup all IPs
adresses = []
with open(filename) as f:
    adresses = f.readlines()
for ip in adresses:
    ip=ip.rstrip("\n")
    location = ipInfo(ip)
    out.write(location+"\n")

out.close()