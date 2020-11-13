from tqdm import tqdm
from itertools import product
from time import sleep
import zipfile
import sys
import argparse

#Menu
parser = argparse.ArgumentParser(description='Howest Zip Cracking T00lK1t')
group = parser.add_mutually_exclusive_group()
group.add_argument("-b", "--bruteforce", action="store_true", help="Select the Bruteforce mode")
group.add_argument("-w", "--wordlist", action="store", dest="wordlist", help="Select the Wordlist, provide wordlist as argument")
parser.add_argument("-l", "--minlenght", action="store", type=int, dest="min_length", default="4", help="Minimum number of characters in password to bruteforce (Default = 4)")
parser.add_argument("-L", "--maxlenght", action="store", type=int, dest="max_length", default="4", help="Maximum number of characters in password to bruteforce (Default = 4)")
parser.add_argument("-f", "--file", action="store", dest="zip_file", default="empty", help="Zip file to crack")
parser.add_argument("-v", "--verbosity", action="store_true", help="increase output verbosity, this will show passwords tried (!! slower cracking !!)")
args = parser.parse_args()

#Banner
print("-------------------------------------")
print("\tHowest Zip Cracking T00lk1t")
print("-------------------------------------")
print("Welcome to the Cybersecurity Fundamentals cracking toolkit - 2020 Quarantaine edition!\n")

# initialize the Zip File object
if args.zip_file == "empty":
    print("[!] Quiting\n[!] Error: No zip file to crack!\n[!]---> See usage for more info:")
    parser.print_usage()
    exit(0)
else:  
    zip_file = zipfile.ZipFile(args.zip_file)


#bruteforce mode
#----------------------
if args.bruteforce:
    print("[+] Bruteforce Mode Selected")
    print("[+] Trying to bruteforce all passwords between "+ str(args.min_length) + " and "+ str(args.max_length) +" characters.")
    
    #chars used in password
    chars = 'abcdefghijklmnopqrstuvwxyz' 
    
    # count the number of possible combinations for the bruteforce attempt
    n_words = 0
    for i in range(args.min_length, args.max_length+1):
        n_words += 26**i
    print("[+] Number of posssible passwords to try:", n_words)
       
    #iterate all possible combinations
    for length in range(args.min_length, args.max_length+1):
        to_attempt = product(chars, repeat=length)
        pbar = tqdm(to_attempt, total=n_words, unit="try")
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
                print("[+] SUCCESS -> Password found:", password)
                exit(0)
    pbar.close()
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
                print("[+] Password found:", password.decode().strip())
                exit(0)
    pbar.close()
    print("[!] Password not found, try other wordlist or bruteforce.")





