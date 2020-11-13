#!/usr/bin/env python3

# Title: Howest Zip Cracking Toolkit
# Version: 0.2 
# Date: Nov 2020
# Author: Hendrik Derre
# Description: This tool tries to crack the passwords from encrypted zip files (using ZipCrypto). For educational purposes only!
# Disclaimer: Only run this tool on files you own or have permission to crack! 

from tqdm import tqdm
from itertools import product
from time import sleep
import zipfile
import sys
import argparse
import os.path

#Menu
parser = argparse.ArgumentParser(description='Zip Cracking Tool - CSF Howest')
group = parser.add_mutually_exclusive_group()
group.add_argument("-b", action="store_true", dest="bruteforce", help="Bruteforce mode")
group.add_argument("-w", action="store", dest="wordlist", help="Wordlist mode - select the wordlist file")
parser.add_argument("-l", action="store", type=int, dest="low_limit", default="4", help="Minimum length of password - Bruteforce mode only (Default = 4)")
parser.add_argument("-u", action="store", type=int, dest="up_limit", default="4", help="Maximum length of password - Bruteforce mode only (Default = 4)")
parser.add_argument("-f", action="store", dest="zip_file", required=True, help="Zip file to crack")
parser.add_argument("-v", action="store_true", dest="verbosity", help="Verbose output - show all passwords tried (= slower cracking!)")
args = parser.parse_args()

#Banner
print("-----------------------------------------------------------")
print("\tHowest Zip Cracking Tool - CSF Howest")
print("-----------------------------------------------------------")
print("Welcome to the Cybersecurity Fundamentals Zip Cracking Toolkit")
print("--> Only run this tool on files you have permission for! <--\n")

#check if a mode is selected
if (args.bruteforce or args.wordlist): 
    #check arguments for bruteforce
    if args.bruteforce:
        if (args.up_limit >= 0 and args.low_limit >= 0 and args.up_limit >= args.low_limit): pass
        else: 
            print("[!] Error: please check minimum '-l' and maximum '-u' password length.")
            parser.print_usage()
            exit(0)
    #check arguments for wordlist
    else:
        if (os.path.isfile(args.wordlist)): pass
        else:
            print("[!] Error: Wordlist does not exist")
            exit(0)

else: 
    print("[!] Error: No mode selected. Please select bruteforce '-b' or wordlist '-w' mode")
    parser.print_usage()
    exit(0)

# initialize the Zip File object
if(os.path.isfile(args.zip_file)):
    zip_file = zipfile.ZipFile(args.zip_file)
else:
    print("[!] Error: zipfile does not exist")
    exit(0)  


#bruteforce mode
#----------------------
if args.bruteforce:
    print("[+] Bruteforce Mode Selected")
    print("[+] Trying all combinations between "+ str(args.low_limit) + " and "+ str(args.up_limit) +" characters.")
    
    #chars used in password
    chars = 'abcdefghijklmnopqrstuvwxyz' 
    
    # count the number of possible combinations for the bruteforce attempt
    n_words = 0
    for i in range(args.low_limit, args.up_limit+1):
        n_words += 26**i
    print("[+] Number of posssible passwords to try:", n_words)
       
    #iterate all possible combinations
    for length in range(args.low_limit, args.up_limit+1):
        print("Bruteforcing: testing password lenght: "+ str(length))
        to_attempt = product(chars, repeat=length)
        bar_max = 26**length
        pbar = tqdm(to_attempt, total=bar_max, unit="try")
        for attempt in pbar:
            password = ''.join(attempt)
    
            if args.verbosity: #if verbose mode is active, show all password tries
                print(password)

            #try if you can unzip with the password, if not continue
            try:
                zip_file.extractall(pwd=password.encode('utf-8')) #needs utf-8 encoding
            except:
                continue
            else:
                pbar.close()                                  
                print("[+] SUCCESS - ZIP FILE CRACKED!")
                print("[+] PASSWORD:", password)
                exit(0)
    sleep(0.5)
    print("[!] Password not found, try more chars or a wordlist")
    exit(0)

#wordlist mode
#------------------------
if args.wordlist:
    print("[+] Wordlist Mode Selected")
    print("[+] Reading from file: " + args.zip_file)

    # count the number of words in this wordlist
    n_words = len(list(open(args.wordlist, "rb")))
    print("[+] Number of passwords in the file:", n_words)

    #iterate all passwords in wordlist
    with open(args.wordlist, "rb") as wordlist:
        pbar = tqdm(wordlist, total=n_words, unit="word")
        for password in pbar:
            if args.verbosity:
                print(password.decode().strip())
            #try if you can unzip with the password, if not continue
            try:
                zip_file.extractall(pwd=password.strip())
            except:
                continue
            else:
                pbar.close()
                print("[+] SUCCESS - ZIP FILE CRACKED!")
                print("[+] PASSWORD:", password.decode().strip())
                exit(0)
    sleep(0.5)
    print("[!] Password not found, try other wordlist or bruteforce.")





