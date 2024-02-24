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

def encryptMessage(key: int, message: str):
    rows = key
    cols = len(message)
    encryptionGrid = [['' for i in range(cols)] for j in range(rows)]
    col = 0
    railIndex = 0
    move = 'down' # to know if we are at the top or bottom of the rails
    for letter in message:
        if move == 'down':
            encryptionGrid[railIndex][col] = letter
            railIndex+=1
        else:
            encryptionGrid[railIndex][col] = letter
            railIndex-=1
        if railIndex == key-1: # we are at the bottom of the rails
            move = 'up'
        elif railIndex == 0: # we are at the top of the rails
            move = 'down'
        col+=1 # After each letter we move to the next col
    cipherText = ''
    for row in encryptionGrid: # join each row together and add it to the ciphertext
        s = ''.join(row)
        cipherText+=s
    return cipherText


def decryptMessage(key: int, message: str):
    # put all dashes in decryption grid 
    decryptionGrid = fillDashes(key, message) 
    # replace dashes by the letters in the ciphertext row by row 
    cipherIndex = 0
    for row in decryptionGrid:
        for letter in row:
            if letter == '_':
                dashIndex = row.index('_')
                row[dashIndex]= message[cipherIndex]
                cipherIndex+=1
   
    # create the plain text by adding letters in zigzag format (similar to encryption)
    plainText = ''
    move = 'down' # to know if we are at the top or bottom of the rails
    col = 0
    railIndex = 0
    cols = len(message)
    while col < cols:
        if move == 'down':
            plainText+=decryptionGrid[railIndex][col] 
            railIndex+=1 # go down the rail 
        else:
            plainText+=decryptionGrid[railIndex][col]
            railIndex-=1 # go up the rail 
        
        if railIndex == key-1: # we are at the bottom of the rails, go up 
            move = 'up'
        elif railIndex == 0: # we are at the top of the rails
            move = 'down'
        col+=1 # After each letter we move to the next col
    return plainText

# function to fill in the dashes into the grid in zigzag format for decryption
def fillDashes(key: int, message: str):
    # put first half of decrypt message in here to make it neater 
    rows = key
    cols = len(message)
    decryptionGrid = [['' for i in range(cols)] for j in range(rows)]
    move = 'down' # to know if we are at the top or bottom of the rails
    col = 0
    railIndex = 0
    # Add all the dashes in zigzag manner based on encryption
    for letter in message:
        if move == 'down':
            decryptionGrid[railIndex][col] = '_'
            railIndex+=1 # go down the rail 
        else:
            decryptionGrid[railIndex][col] = '_'
            railIndex-=1 # go up the rail 
        
        if railIndex == key-1: # we are at the bottom of the rails, go up 
            move = 'up'
        elif railIndex == 0: # we are at the top of the rails
            move = 'down'
        col+=1 # After each dash we move to the next col
    return decryptionGrid

def test():
    assert decryptMessage(2, encryptMessage(2, "SECRET")) == "SECRET"
    assert decryptMessage(3, encryptMessage(3, "CIPHERS ARE FUN")) == "CIPHERS ARE FUN"
    assert decryptMessage(4, encryptMessage(4, "HELLO WORLD")) == "HELLO WORLD"
    
    

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
