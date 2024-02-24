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
Assignment 7 Problem 1
"""


from sys import flags
import string
import a1p3 



def antiKasiski(key: str, plaintext: str):
    """
    Thwart Kasiski examination 
    """
    ptList = list(plaintext) # list of plain text (we'll keep adding 'X' to this)
    # print(ptList)
    keepChecking = True
    seqIndex = 0 # index of the repeated seq
    while keepChecking:
        cipherText = encrypt(plaintext,key) #ciphertext
        seq = makeSeq(cipherText,seqIndex) # make 3 letter sequnces from the index provided
        # repeatedSeq = [] # all the repeated sequences
        for s in seq: # for each 3 letter subsequence 
            if seq.count(s)> 1:
                # repeatedSeq.append(s)
                seqIndex = cipherText.find(s) # find the index the sequence occurs
                Xindex = seqIndex + 3 # index to actually place the 'X'
                ptList.insert(Xindex,'X')
                plaintext = ''.join(ptList)
                keepChecking = True
                break
            else:
                keepChecking = False 
    return cipherText

def makeSeq(text,index):
    # index is from where to start from
    n=3
    seq = []
    for i in range(index,len(text)): # for each letter
        if i+n <= len(text): # make sure we have n more letters to check 
            nG = ''
            for j in range(n): # make the ngram
                nG+=text[i+j] # add the letters infront up to n
            seq.append(nG)
    return seq


def encrypt(message: str, key: str):
    SHIFTDICT, LETTERDICT = a1p3.get_map()
    LETTERS = ''.join([u+l for u, l in zip(string.ascii_uppercase, string.ascii_lowercase)])
    
    keywordList = list(key) # converting the key string passed into a list for my convenience
    shiftIndex = 0 # to track the index of the current shift letter in the keyword so we know when to go back to the begining
    keywordLength = len(keywordList) # length of the keyword 
    messageLetters = list(message) # converting the string passed into a list for my convenience
    encryptList = [] # list of the letters in the encrypted message
    for i in range(len(messageLetters)):
        if messageLetters[i].isalpha(): # if it's a letter  
            if shiftIndex == keywordLength: # to check if we're still in the range of the keyword, if we aren't we set shiftIndex to 0 (back to the begining of the keyword)
                shiftIndex = 0
            # shift based on the current position we're in the keyWord 
            shift = SHIFTDICT[keywordList[shiftIndex]]
            # increment the index to go to the next letter in the keyword to use as the shift
            shiftIndex+=1
            # get the index of that letter in LETTERS
            num = LETTERS.find(messageLetters[i])
            # add shift to num (index) to calculate the total shift needed 
            calculatedShift = num + shift
            # handle the wrap-around if calculated shift is larger than the length of LETTERS
            if calculatedShift >= len(LETTERS):
                calculatedShift = calculatedShift - len(LETTERS)
            #add the encrypted letter to the list    
            encryptList.append(LETTERS[calculatedShift])
        else: # it's not a letter  
            encryptList.append(messageLetters[i])
    # convert to string to return
    encryptedMessage = "".join(encryptList)
    return encryptedMessage

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    

# Invoke test() if called via `python3 a7p1.py`
# but not if `python3 -i a7p1.py` or `from a7p1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
