#!/usr/bin/python3

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
CMPUT 331 Assignment 1 Student Solution
September 2023
Author: <Your name here>
"""


from curses.ascii import isalpha
import string
from sys import flags


LETTERS = ''.join([u+l for u, l in 
    zip(string.ascii_uppercase, string.ascii_lowercase)])

# function to create the mapping of the respective letters to ther shift(index) and vice versa
def get_map(letters=LETTERS):
    map1 = {}
    map2 = {}
    for i in range(len(letters)):
        # set the letter (key) to it's shift(value) in the first dictionary 
        map1[letters[i]] = i 
        # set the shift (key) to it's letter(value) in the second dictionary 
        map2[i] = letters[i]
    return map1,map2
   

def encrypt(message: str, key: str):
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
   

def decrypt(message: str, key: str):
    keywordList = list(key) # converting the key string passed into a list for my convenience
    shiftIndex = 0 # to track the index of the current shift letter in the keyword so we know when to go back to the begining
    keywordLength = len(keywordList) # length of the keyword 
    messageLetters = list(message) # converting the string passes into a list for my convenience
    decryptList = [] # list of the letters in the decrypted message
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
            # subtract shift from num (index) to calculate the total shift
            calculatedShift = num - shift
            # handle the wrap-around if calculated shift is less than the length of LETTERS
            if calculatedShift < 0:
                calculatedShift = calculatedShift + len(LETTERS)
            # add the decrypted letter to the list    
            decryptList.append(LETTERS[calculatedShift])
        else: # it's not a letter  
            # add the decrypted letter to the list
            decryptList.append(messageLetters[i])
    # convert to string to return
    decryptedMessage = "".join(decryptList)
    return decryptedMessage

def test():
    global SHIFTDICT, LETTERDICT 
    SHIFTDICT, LETTERDICT = get_map()
    assert decrypt(encrypt("foo", "g"), "g") == "foo"
    
if __name__ == "__main__" and not flags.interactive:
    test()
