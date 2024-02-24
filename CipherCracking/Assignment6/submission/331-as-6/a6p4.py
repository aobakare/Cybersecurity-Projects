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
Problem 4
"""
ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
from sys import flags
import freqAnalysis
from a6p1 import ngramsFreqsFromFile
from a6p3 import bestSuccessor

def breakSub(cipherFile: str , textFile: str, n: int) -> None:
    """
    Inputs:
        cipherFile: 
            'text_finnegan_cipher.txt' for implementation
            'text_cipher.txt' for submission
        textFile: 'wells.txt'
    Outputs:
        'text_finnegan_plain.txt' for implementation
        'text_plain.txt' for submission
    """


    cFile = open(cipherFile,'r')
    cipherText = cFile.read()
    mapping = freqDict(cipherText)
    ngramFreq = ngramsFreqsFromFile(textFile,n)
    keepChecking  = True 
    map1 = bestSuccessor(mapping,cipherText,ngramFreq,n)
    while keepChecking:
        map2 = bestSuccessor(map1,cipherText,ngramFreq,n)
        if map1 == map2:
            break
        else:
            map1 = map2
  
    decipherment = ''
    for letter in cipherText:
        if letter.isalpha():
            decipherment += map1[letter]
        else:
            decipherment += letter
    outputFile = open('test_plain.txt','w') 
    outputFile.write(decipherment)



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
    for i in range(len(freqOrder)):
        freqDictionary[freqOrder[i]] = ETAOIN[i]
    freqDictionary[' '] = ' ' # ADDED THIS BECAUSE OF KEY ERROR IN a6p2.py
    return freqDictionary

# to check which occurs first 
def firstLetter(letter1,letter2):
    if letter1.lower() < letter2.lower():
        return letter1,letter2
    else:
        return letter2,letter1
def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    breakSub('text_cipher.txt','wells.txt',3)
if __name__ == "__main__" and not flags.interactive:
    test()