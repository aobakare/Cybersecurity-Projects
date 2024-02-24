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
CMPUT 331 Assignment 3 Student Solution
September 2023
Author: <Abdulrahman Bakare>
"""

def random_generator(a, b, c, m, r0, r1, n):
    rList = [r0,r1]
    for i in range(n):
        r = ((a*rList[i+1])+(b*rList[i])+c) % m
        rList.append(r)
    
    # remove the first 2 elements because we don't want r0 and r1
    rList.pop(0)
    rList.pop(0)
    return rList 





def test():
    assert random_generator(3, 5, 9, 16, 11, 6, 3) == [2, 13, 10]
    assert random_generator(22695477, 77557187, 259336153, 9672485827, 42, 51, 8) == [4674207334, 3722211255, 3589660660, 1628254817, 8758883504, 7165043537, 4950370481, 2261710858]
    assert random_generator(2**31-5, 743, 549, 2**64 - 1, 97, 101, 8) == [216895920563, 4611839799731136226, 4610466323469147181, 6003130118321022275, 14149176448272843437, 14229211546334517160, 10244020959373064815, 2515976774685790769]
    assert random_generator(1128889, 1023, 511, 222334565193649, 65535, 329, 8) == [438447297, 50289200612813, 17962583104439, 47361932650166, 159841610077391, 19587857129781, 111993173627854, 7567964632208]
from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()