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
Problem 3
"""

from sys import flags
from copy import deepcopy
from a6p2 import keyScore

def bestSuccessor(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> dict:
    keyList = list(mapping.keys())
    bestScore = keyScore(mapping,ciphertext,frequencies,n) # the initial best score would be the score of the original m
    maxSuccessor = mapping # the intial successor with the best score would be the original m
    for i in range(len(keyList)):
        mPrime = deepcopy(mapping) # copy mapping 
        v1 = mapping[keyList[i]] # first value to be swapped
        for j in range(len(keyList)):
            if i < j: # we shouldn't look at the same charcater to swap
                v2 = mapping[keyList[j]] # 2nd value to be swapped
                if keyList[i] != ' ' and keyList[j] != ' ':
                    mPrime[keyList[i]] = v2 # swap key1 value to value2 
                    mPrime[keyList[j]] = v1 # swap key2 value to value1
                mPrimeScore = keyScore(mPrime,ciphertext,frequencies,n) #get m' Score 
                if mPrimeScore > bestScore: # set bestscore to higher value and change the maximum successor 
                    bestScore = mPrimeScore
                    maxSuccessor = mPrime
                elif mPrimeScore == bestScore: # break tie and set higher value 
                    maxSuccessor= breakKeyScoreTie(mapping,mPrime,maxSuccessor)
                    bestScore = keyScore(maxSuccessor,ciphertext,frequencies,n)
                mPrime = deepcopy(mapping) # reset mPrime to original mPrime to do next swap
    return maxSuccessor
    

def breakKeyScoreTie(originalMapping, successorMappingA, successorMappingB):
    """
    Break the tie between two successor mappings that have the same keyscore

    originalMapping: mapping the the other parameters are successors to
    successorMappingA: mapping that has had two keys swapped
    successorMappingB: mapping that has had two other keys swapped

    Example usage:
    originalMapping = {"A": "A", "B": "B", "C": "C"}
    # Mapping with B and C switched
    successorMappingA = {"A": "A", "B": "C", "C": "B"}
    # Mapping with A and C switched
    successorMappingB = {"A": "C", "B": "B", "C": "A"}

    # AC < BC so this function will return successorMappingB
    assert breakKeyScoreTie(originalMapping, successorMappingA, successorMappingB) == successorMappingB
    """
    aSwapped = "".join(sorted(k for k, v in (
        set(successorMappingA.items()) - set(originalMapping.items()))))
    bSwapped = "".join(sorted(k for k, v in (
        set(successorMappingB.items()) - set(originalMapping.items()))))
    return successorMappingA if aSwapped < bSwapped else successorMappingB

def test():
    
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    assert breakKeyScoreTie({"A": "A", "B": "B", "C": "C"}, {"A": "A", "B": "C", "C": "B"}, {
                            "A": "C", "B": "B", "C": "A"}) == {"A": "C", "B": "B", "C": "A"}
    assert breakKeyScoreTie({"A": "A", "B": "B", "C": "C", "D": "D"}, {
                            "A": "B", "B": "A", "C": "C", "D": "D"}, {"A": "A", "B": "B", "C": "D", "D": "C"}) == {"A": "B", "B": "A", "C": "C", "D": "D"}
   
if __name__ == "__main__" and not flags.interactive:
    test()


    