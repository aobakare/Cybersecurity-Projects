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

def decryptMessage(key: List[int], message: str):
    messageLen = len(message)
    rows = getMax(key)
    cols = math.ceil(messageLen /rows) # number of cols always needed is the messageLen/rows rounded up
    decryptionGrid = addShade(key,message) # create decryptionGrid with shaded boxes added where required 
    
    # to fill in the letters into the grid from left to right, the row we fill will be according to the order given in the key list  
    letterIndex = 0 # to keep track of where we are in the text 
    for row in key: # for each row in the key 
        col = 0
        while col < cols: # to check if we're at the end of the col 
            if decryptionGrid[row-1][col] != '*': # only add to boxes not shaded (-1 because of index starts from 0 not 1)
               decryptionGrid[row-1][col] = message[letterIndex]
               letterIndex+=1     
            col+=1 # increment col position 
   
    # make the plain text
    plainText = ''
    for col in range(cols): # for each col
        for row in range(rows): # for each box in that col
            if decryptionGrid[row][col] != '*': # if not shaded 
                plainText+=decryptionGrid[row][col] # add the letter to the plain text 
    return plainText

#function to add shaded boxes 
def addShade(key: List[int], message: str):
    messageLen = len(message)
    rows = getMax(key)
    cols = math.ceil(messageLen /rows) # number of cols always needed is the messageLen/rows rounded up
    shaded = (rows*cols) - messageLen
    decryptionGrid = [['' for i in range(cols)] for j in range(rows)]
    shaded = (rows*cols) - messageLen
    rowToShade = rows-1 # -1 because of index starts from 0 not 1
    colToShade = cols-1
    while shaded >= 1: # while theres boxes to shade 
        decryptionGrid[rowToShade][colToShade] = '*' # add shade
        rowToShade-=1 # move up the row
        if rowToShade == 0: # we are at the top of the rails
            rowToShade = rows-1
            colToShade-=1 # After each letter we move to the next col
        shaded-=1 # redeuce number of boxes to shade  
    return decryptionGrid

# function to get the max 
def getMax(key: List[int]):
    max = key[0]
    for i in key:
        if max < i:
            max = i
    return max

def test():
    assert decryptMessage([2, 4, 1, 5, 3], "IS HAUCREERNP F") == "CIPHERS ARE FUN"

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
