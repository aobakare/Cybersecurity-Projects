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
Problem 2
"""

from curses.ascii import isalpha
from sys import flags
import numpy as np
def evalDecipherment(text1: str, text2: str) -> [float, float]:
    """
    docstring
    """
    charType = []
    totalChars = []
    for letter in text1:
        if letter.isalpha()  and letter not in charType:
            charType.append(letter)
    charTypeNo = len(charType)
    
    for letter in text1:
        if letter.isalpha(): 
            totalChars.append(letter)
    totalCharsNo = len(totalChars)
    
    text1List = list(text1)
    text2List = list(text2)
    count = 0
    checked = [] # to keep track of the letters we have checked 
    for i in range(len(text1List)):
        if text1List[i].isalpha() and text1List[i].lower() != text2List[i].lower() and text1List[i] not in checked:
            checked.append(text1List[i])
            count+=1
    keyAccuracy = (charTypeNo - count)/charTypeNo
  
    count = 0
    for i in range(len(text1List)):
        if text1List[i].isalpha() and text1List[i].lower() != text2List[i].lower():
            checked.append(text1List[i])
            count+=1
    decipherAccuracy = (totalCharsNo - count)/totalCharsNo
    return [keyAccuracy,decipherAccuracy]

def test():
    # print(evalDecipherment("this is an example", "tsih ih an ezample"))
    "Run tests"
    np.testing.assert_array_almost_equal(evalDecipherment("this is an example", "tsih ih an ezample") , [0.7272727272727273, 0.7333333333333333])
    np.testing.assert_almost_equal(evalDecipherment("the most beautiful course is 331!", "tpq munt bqautiful cuurnq in 331!") , [0.7142857142857143, 0.625])
if __name__ == '__main__' and not flags.interactive:
    test()
