from tqdm import tqdm
from itertools import product
import zipfile
import sys
import argparse

#Menu
parser = argparse.ArgumentParser(description='Howest Zip Cracking T00lK1t')
group = parser.add_mutually_exclusive_group()
group.add_argument("-b", "--bruteforce", action="store_true", help="Select the Bruteforce mode")
group.add_argument("-w", "--wordlist", action="store", dest="wordlist", help="Select the Wordlist")
parser.add_argument("-l", "--minlenght", action="store", type=int, dest="min_length", default="4", help="Minimum number of characters to try to bruteforce (Default = 4)")
parser.add_argument("-L", "--maxlenght", action="store", type=int, dest="max_length", default="4", help="Max number of characters to try to bruteforce (Default = 4)")
parser.add_argument("-f", "--file", action="store", dest="zip_file", default="empty", help="Zip file to crack")
args = parser.parse_args()


# initialize the Zip File object
if args.zip_file == "empty":
    print("!!Quiting\nError: No zip file to crack!\n---> See usage for more info:")
    parser.print_usage()
    exit(0)
else:  
    zip_file = zipfile.ZipFile(args.zip_file)


#bruteforce mode
#----------------------
if args.bruteforce:
    print("-------------------------------------")
    print("\tbruteforce mode")
    print("-------------------------------------")

    #chars used in password
    chars = 'abcdefghijklmnopqrstuvwxyz' 
    
    # count the number of possible combinations for the bruteforce attempt
    n_words = 0
    for i in range(args.min_length, args.max_length+1):
        n_words += 26**i
    print("Total passwords to test:", n_words)
    
    for length in range(args.min_length, args.max_length+1):
        to_attempt = product(chars, repeat=length)
        for attempt in tqdm(to_attempt, total=n_words, unit="try"):
            password = ''.join(attempt)
            try:
                zip_file.extractall(pwd=password.encode('utf-8')) #needs utf-8 encoding
            except:
                continue
            else:
                print("[+] Password found:", password)
                exit(0)
    print("[!] Password not found, try more chars or wordlist")
    exit(0)

#wordlist mode
#------------------------
if args.wordlist:
    print("-------------------------------------")
    print("\twordlist mode")
    print("-------------------------------------")

    # count the number of words in this wordlist
    n_words = len(list(open(args.wordlist, "rb")))
    print("Number of passwords in the file:", n_words)

    with open(args.wordlist, "rb") as wordlist:
        for word in tqdm(wordlist, total=n_words, unit="word"):
            try:
                zip_file.extractall(pwd=word.strip())
            except:
                continue
            else:
                print("[+] Password found:", word.decode().strip())
                exit(0)
    print("[!] Password not found, try other wordlist or bruteforce.")





