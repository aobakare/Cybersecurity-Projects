#!/usr/bin/env python3

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
Nomenclator cipher
"""
from pydoc import plain
import re, simpleSubCipher,random


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def translateMessage(key: str, message: str, codebook: dict, mode: str):
    """
    Encrypt or decrypt using a nomenclator.
    Takes a substitution cipher key, a message (plaintext or ciphertext),
    a codebook dictionary, and a mode string ('encrypt' or 'decrypt')
    specifying the action to be taken. Returns a string containing the
    ciphertext (if encrypting) or plaintext (if decrypting).
    """
    wordList =  message.split()
    # for word in word
    if mode == 'encrypt':
        codebook = {k.lower(): v for k, v in codebook.items()} # makes all the keys lowercase to make my checking easier 
        for i in range(len(wordList)): # convert any codeword to their respective symbol
            if removePunctuations(wordList[i].lower()) in codebook: # if the word without any punctuation is in the codebook
                noPunctWord = removePunctuations(wordList[i].lower()) # remove punctuation
                if noPunctWord != wordList[i].lower(): # there was a punctuation we need to add back at the end 
                    punct = wordList[i][len(wordList[i]-1)] # the punctuation at the end of the string            
                    wordList[i] = random.choice(codebook[wordList[i].lower()]) # get a random corresponding number of that key
                    wordList[i] += punct # add the punctuation at the end 
                else: # no punctuation 
                   wordList[i] = random.choice(codebook[wordList[i].lower()]) # get a random corresponding number of that key 

        cipherText = ' '.join(wordList) # convert back to string to do simpleSubCipher Encryption
        cipherText = simpleSubCipher.encryptMessage(key,cipherText) # encrypt the remaining letters with simpleSubCipher 
        return cipherText
    else:
        message = simpleSubCipher.decryptMessage(key,message) # decrypt all the letters in the cipher text intially 
        wordList =  message.split() # to change the code word values to their actual code word 
        dictKeyList = list(codebook.keys()) # get all the keys into a list 
        dictValueList = list(codebook.values()) # get all the values into a list 
        for i in range(len(wordList)): # check all words to see if we have a codeword value 
            for value in dictValueList:
                if removePunctuations(wordList[i]) in value: # we need to check without punctuation so it would be accurate
                    noPunctWord = removePunctuations(wordList[i]) # remove punctuation
                    if noPunctWord != wordList[i]: # there was a punctuation we need to add back at the end
                        punct = wordList[i][len(wordList[i]-1)] # the punctuation at the end of the string
                        valueIndex = dictValueList.index(value) # get the index of the value 
                        wordList[i] = dictKeyList[valueIndex]   # set the value to its codeword (keylist and ValueList will have identical indices)
                        wordList[i] += punct # add the punctuation at the end 
                    else: # no puntuation to be added
                        valueIndex = dictValueList.index(value) # get the index of the value 
                        wordList[i] = dictKeyList[valueIndex]   # set the value to its codeword (keylist and ValueList will have identical indices)        
        plainText = ' '.join(wordList)
        return plainText

    
    
def encryptMessage(key: str, codebook: dict, message: str):
    return translateMessage(key, codebook, message, 'encrypt')


def decryptMessage(key: str, codebook: dict, message: str):
    return translateMessage(key, codebook, message, 'decrypt')

def removePunctuations(word:str): # to remove punctuations from word 
    pattern = r'[^\w\s]' # not word character (letter, digit or underscore) or space
    newWord= re.sub(pattern, '', word)
    return newWord

def test():
    # Provided test.
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    message = 'At the University of Alberta, examinations take place in December and April for the Fall and Winter terms.'
    codebook = {'university':['1', '2', '3'], 'examination':['4', '5'], 'examinations':['6', '7', '8'], 'WINTER':['9']}
    cipher = translateMessage(key, message, codebook, 'encrypt')
    print(cipher)
    translateMessage(key, cipher, codebook, 'decrypt')
    print(translateMessage(key, cipher, codebook, 'decrypt'))
    # End of provided test.

if __name__ == '__main__':
    test()

