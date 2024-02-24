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
Assignment 7 Problems 2, 3, and 4
"""

import re
from sys import flags
import statistics


def stringIC(text: str):
    """
    Compute the index of coincidence (IC) for text
    """
    checked  = []
    countDict = {}
    textList = list(text)
    for letter in text:
        if letter not in checked:
            countDict[letter] = textList.count(letter)
            checked.append(letter)
    N = len(text)
    summation = 0
    for letter in checked:
        summation += countDict[letter] * (countDict[letter] -1)
    IC = summation / (N * (N-1))
    return IC

def subseqIC(ciphertext: str, keylen: int):
    """
    Return the average IC of ciphertext for 
    subsequences induced by a given a key length
    """
    subSeq = []
    IC = [] 
    for i in range(1,keylen+1):
        subSeq.append(getNthSubkeysLetters(i,keylen,ciphertext))
    for seq in subSeq:
        IC.append(stringIC(seq))
    return statistics.mean(IC)
    


def keyLengthIC(ciphertext: str, n: int):
    """
    Return the top n keylengths ordered by likelihood of correctness
    Assumes keylength <= 20
    """
    ICdict = {}
    for i in range (1,21):
        ICdict[i] = subseqIC(ciphertext,i)
    ICdict = sorted(ICdict.items(), key=lambda x:x[1],reverse=True)
    result = []
    for i in range(0,5):
        if ICdict[i][1] == ICdict[i+1][1]: # to break ties
            lesser = ICdict[i][0]
            if lesser > ICdict[i+1][0]:
                lesser = ICdict[i+1][0]
                result.append(lesser)
        else:
            result.append(ICdict[i][0])
    return result

def getNthSubkeysLetters(nth: int, keyLength: int, message: str):
    # Returns every nth letter for each keyLength set of letters in text.
    # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'

    # Use a regular expression to remove non-letters from the message:
    message = re.compile('[^A-Z]').sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def test():
    "Run tests"
    stringIC("ABA")
    # assert stringIC("ABA") == 1 / 3
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
   
# Invoke test() if called via `python3 a7p234.py`
# but not if `python3 -i a7p234.py` or `from a7p234 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
