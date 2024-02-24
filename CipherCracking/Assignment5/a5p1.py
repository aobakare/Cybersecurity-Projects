#!/usr/bin/env python3

#---------------------------------------------------------------
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
#---------------------------------------------------------------

"""
Subsititution cipher frequency analysis
"""
ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
from curses.ascii import isalpha
from sys import flags
from collections import Counter # Helpful class, see documentation or help(Counter)
import freqAnalysis

def freqDict(ciphertext: str) -> dict:
    """
    Analyze the frequency of the letters
    """
    letterCount  =  freqAnalysis.getLetterCount(ciphertext)
    freqOrder = list(freqAnalysis.getFrequencyOrder(ciphertext))
    freqDictionary = {}
    checked = [] # to track letters have already been checked 
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            letter1 = ciphertext[i]
            if letter1 not in checked:
                checked.append(letter1) # add to already checked 
            letter1Count = letterCount[letter1] # get freq of letter 1
            for j in range(1,len(ciphertext)):
                if ciphertext[j].isalpha():
                    letter2 = ciphertext[j]
                    letter2Count = letterCount[letter2]
                    if letter1Count == letter2Count and letter2 not in checked: #if the freq are the same we want to ensure the letter that comes first in the alphabet takes precedence 
                        first,second = firstLetter(letter1,letter2) # return the first letter and second letter 
                        freqOrder[freqOrder.index(first)], freqOrder[freqOrder.index(second)] = freqOrder[freqOrder.index(second)], freqOrder[freqOrder.index(first)] # switch positions
    freqOrder = ''.join(freqOrder)
    for i in range(len(checked)):
        freqDictionary[freqOrder[i]] = ETAOIN[i]
    return freqDictionary

def freqDecrypt(mapping: dict, ciphertext: str) -> str:
    """
    Apply the mapping to ciphertext
    """
    plainText = ''
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            plainText += mapping[ciphertext[i]]
        else:
            plainText += ciphertext[i]
    return plainText

# to check which occurs first 
def firstLetter(letter1,letter2):
    if letter1.lower() < letter2.lower():
        return letter1,letter2
    else:
        return letter2,letter1

def test():
    "Run tests"
    assert type(freqDict("A")) is dict
    assert freqDict("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")["A"] == "E"
    assert freqDict("AABBA")['B'] == "T"
    assert freqDict("-: AB CD AH")['A'] == "E"
    assert freqDecrypt({"A": "E", "Z": "L", "T": "H", "F": "O", "U": "W", "I": "R", "Q": "D"}, "TAZZF UFIZQ!") == "HELLO WORLD!"


# Invoke test() if called via `python3 a5p1.py`
# but not if `python3 -i a5p1.py` or `from a5p1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
