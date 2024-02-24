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

def crack_rng(m, sequence):
    r2, r3, r4, r5, r6 = tuple(sequence)
# formulas based in my solution for problem 3
    A = (r5-r4)*findModInverse(r3-r2,m) 
    B = (r4-r3)*findModInverse(r3-r2,m)
    C = (r6-r5)*findModInverse(r4-r3,m)
    D = (r5-r4)*findModInverse(r4-r3,m)

    a = ((C-A)*findModInverse(D-B,m)) % m
    b = (C - (a*D)) % m
    c = (r4-(a*r3)-(b*r2)) % m

    return [a,b,c]

# from cryptomath.py from CrackingCodesFiles
def findModInverse(a, m):
    # Return the modular inverse of a % m, which is
    # the number x such that a*x % m = 1

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # Note that // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
def test():
    assert crack_rng(17, [14, 13, 16, 3, 13]) == [3, 5, 9]
    assert crack_rng(9672485827, [4674207334, 3722211255, 3589660660, 1628254817, 8758883504]) == [22695477, 77557187, 259336153]
    assert crack_rng(101, [0, 91, 84, 16, 7]) == [29, 37, 71]
    assert crack_rng(222334565193649,[438447297,50289200612813,17962583104439,47361932650166,159841610077391]) == [1128889, 1023, 511]
    
from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()