#!/usr/bin/python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2023 <<Abdulrahman Bakare>>
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
CMPUT 331 Assignment 2 Student Solution
September 2023
Author: <Abdulrahman Bakare>
"""

from typing import List
import math

def encryptMessage(key: List[int], message: str):
    # get the largest number in the key list to get the number of cols needed 
    numberOfCols = getMax(key)
    for col in key:
        if numberOfCols < col:
            numberOfCols = col
    messageLen = len(message)
    rows = math.ceil(messageLen /numberOfCols) # number of rows always needed is the messageLen/numberOfCols rounded up
    messageEnd = 0
    encryptionGrid = [['' for i in range(numberOfCols)] for j in range(rows)]
    
    # fill in the encryption grid 
    for row in range(rows):
        for col in range(numberOfCols):
            if messageEnd != messageLen: # if were not at the end of the message 
                encryptionGrid[row][col] = message[messageEnd]
                messageEnd+=1
            else: # if the message is done, shade(*) the unused boxes
               encryptionGrid[row][col] = '*'
    
    # produce the cipherText based on the order of columns provided in the key list
    cipherText = ''
    for col in key:
        for row in range(rows):
            # col-1 because of index starts from 0 not 1
            if encryptionGrid[row][col-1] != '*': # ignore the shaded boxes when going down the columns
                cipherText+=encryptionGrid[row][col-1]
    return cipherText
    
# function to get the max 
def getMax(key: List[int]):
    max = key[0]
    for i in key:
        if max < i:
            max = i
    return max
        

def test():
    assert encryptMessage([2, 4, 1, 5, 3], "CIPHERS ARE FUN") == "IS HAUCREERNP F"
    assert encryptMessage([1, 3, 2], "ABCDEFG") == "ADGCFBE"
    assert encryptMessage([2, 1], "HELLO WORLD") == "EL OLHLOWRD"
    
from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
