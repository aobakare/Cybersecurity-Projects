#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2023 <<Insert your name here>>
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
# ---------------------------------------------------------------

"""
Assignment 9 Problem 1
"""

from sys import flags
from typing import Tuple
import primeNum 
import cryptomath

def finitePrimeHack(t: int, n: int, e: int) -> Tuple[int, int, int]:
    """
    Hack RSA assuming there are no primes larger than t
    """
    primes = primeNum.primeSieve(t) # CHANGE 100 TO t
    p=0
    q=0
    for prime in primes:
        no = n % prime
        if no == 0:
            p = prime
            # print(prime)
            q = int(n/p)
            if primeNum.isPrime(q):
                # print(q)
                break
    dMod = (p-1)*(q-1)
    d = cryptomath.findModInverse(e,dMod)
    return (p,q,d)


def test():
    "Run tests"
    assert finitePrimeHack(100, 493, 5) == (17, 29, 269)
    assert finitePrimeHack(2**20,584350822261,567347) == (743221, 786241, 454279775483)
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    # finitePrimeHack(100, 493, 5)
    # finitePrimeHack(2**16,2604135181,1451556085)
    
    # # for problem 2 
    # hackedList = []
    # #1
    # with open('1_pubkey.txt','r') as file:
    #     text = file.read()
    #     text = text.split(',')
    #     # print(text)
    #     hacked = finitePrimeHack(2**int(text[0]),int(text[1]),int(text[2]))
    #     # print(hacked)
    #     hackedList.append(hacked)
    # #2
    # with open('2_pubkey.txt','r') as file:
    #     text = file.read()
    #     text = text.split(',')
    #     # print(text)
    #     hacked = finitePrimeHack(2**int(text[0]),int(text[1]),int(text[2]))
    #     # print(hacked)
    #     hackedList.append(hacked)

    # #3
    # with open('3_pubkey.txt','r') as file:
    #     text = file.read()
    #     text = text.split(',')
    #     # print(text)
    #     hacked = finitePrimeHack(2**int(text[0]),int(text[1]),int(text[2]))
    #     # print(hacked)
    #     hackedList.append(hacked)

    # #4
    # with open('4_pubkey.txt','r') as file:
    #     text = file.read()
    #     text = text.split(',')
    #     # print(text)
    #     hacked = finitePrimeHack(2**int(text[0]),int(text[1]),int(text[2]))
    #     # print(hacked)
    #     hackedList.append(hacked)  
    
    # #5
    # with open('5_pubkey.txt','r') as file:
    #     text = file.read()
    #     text = text.split(',')
    #     # print(text)
    #     hacked = finitePrimeHack(2**int(text[0]),int(text[1]),int(text[2]))
    #     # print(hacked)
    #     hackedList.append(hacked)
    # print(hackedList)

    # #write results to a9.txt
    # with open('a9.txt','w+') as file:
    #     for hacked in hackedList:
    #         text = '({p},{q},{d})\n'.format(p = hacked[0],q= hacked[1],d=hacked[2])
    #         file.write(text)

# Invoke test() if called via `python3 a9p1.py`
# but not if `python3 -i a9p1.py` or `from a9p1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
