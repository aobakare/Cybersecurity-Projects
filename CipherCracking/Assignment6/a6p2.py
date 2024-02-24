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

from sys import flags

def keyScore(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> float:
    # do decipherment
    decipherment = ''
    for letter in ciphertext:
        if letter.isalpha() or letter == ' ':
            decipherment += mapping[letter]
        else:
            decipherment += letter
    # get count using my function 
    countDict, fOfg = ngramsFreqsFromFile(decipherment,n)
    # calulate the score
    score = 0
    for key in countDict:
        c = countDict[key] # get the count 
        f = 0
        if key in frequencies: # if ngram in frequency dictionary get the frequency 
            f = frequencies[key]
        score+= c*f
    return score  

def ngramsFreqsFromFile(text: str, n: int) -> dict:
    """
    textFile: 'wells.txt'
    """
    nGramList = []
    #make ngrams
    for i in range(0,len(text)): # for each letter
        if i+n <= len(text): # make sure we have n more letters to check 
            nG = ''
            for j in range(n): # make the ngram
                nG+=text[i+j] # add the letters infront up to n
            nGramList.append(nG)
    #count and calculate ngrams
    checked = [] #to store the n grams we checked
    countDict = {}
    nGramDict = {}
    for ngram in nGramList:
        if ngram not in checked:
            count = nGramList.count(ngram) # count the number of occurences for that ngram
            countDict[ngram] = count
            nGramDict[ngram] = float(count/len(nGramList)) # calculate the relative frequency 
            checked.append(ngram) # add this ngram to checked so we don't count it again 
    return countDict , nGramDict

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

if __name__ == "__main__" and not flags.interactive:
    test()





