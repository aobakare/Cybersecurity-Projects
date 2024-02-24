#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.1
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
Assignment 8 Problems 1, 2 and 3
"""
import itertools
from sys import flags
import a7p234 as a7
import re
import vigenereCipher

# English letter frequencies for calculating IMC (by precentage)
ENG_LETT_FREQ = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 
                 'R': 5.99,  'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 
                 'G': 2.02,  'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 
                 'Q': 0.10,  'Z': 0.07}

def getLetterFrequency(message):
    # Returns a dictionary of letter frequencies in the message
    # Divide each letter count by total number of letters in the message to get it's frequency
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 
                   'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 
                   'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 
                   'Y': 0, 'Z': 0}
    checked  = []
    ListOfLetters = list(message)
    for letter in message:
        if letter not in checked:
            letterCount[letter] = (ListOfLetters.count(letter)/len(message)) 
            checked.append(letter)
    return letterCount

def getSubsequences(ciphertext, keylen):
    '''This function takes in a ciphertext as a string and a key length as a int for its parameters
    This function will return list containing the characters in each subsequence'''
    subsequences = []
    for i in range(keylen):
        subsequences.append(a7.getNthSubkeysLetters(i+1,keylen,ciphertext))
    return subsequences

def calculateTopIMC(subsequence):
    ''' Given a string, this function will calculate and return a list containing all 26 keys and their IMC values
    Return a list of tuples containing key, IMC pairs from largest IMC to smallest'''
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    topIMC=[]
    for i in range(len(LETTERS)):
        key = LETTERS[i]
        decipher = decrypt(subsequence,key)
        imc = getIMC(decipher)
        topIMC.append((key,imc))
        topIMC.sort(key = lambda x:x[1], reverse=True)
    return topIMC

def decrypt(cipherText:str , key:str):
    '''this function will apply ceaser shift to decrypt the ciphertext based on the key provided
     Using method used in ceaserCipher.py'''
    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = SYMBOLS.index(key)
    translated = ''
    for symbol in cipherText:
        # Note: Only symbols in the `SYMBOLS` string can be encrypted/decrypted.
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)
            translatedIndex = symbolIndex - key

            # Handle wrap-around, if needed:
            if translatedIndex >= len(SYMBOLS):
                translatedIndex = translatedIndex - len(SYMBOLS)
            elif translatedIndex < 0:
                translatedIndex = translatedIndex + len(SYMBOLS)
            translated = translated + SYMBOLS[translatedIndex]
    return translated

def getIMC(subseq:str):
    """
    Compute the index of mutual coincidence (IMC) of a subsequence
    """
    subseqFreq = getLetterFrequency(subseq)
    checked  = []
    summation = 0
    for letter in subseq:
        if letter not in checked:
            summation += subseqFreq[letter] * (ENG_LETT_FREQ[letter]/100)
            checked.append(letter)
    return summation

def decryptVigenere(ciphertext, key):
    '''This function takes in a vigenere ciphertext and it's key as the parameters. 
    It is decrypted using vignereCipher.py'''
    
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    decryption = vigenereCipher.decryptMessage(key,ciphertext)
    return decryption

def vigenereKeySolver(ciphertext: str, keylength: int):
    """
    return a list of the ten most likely keys
    """
    # Remove non characters in ciphertext
    ciphertext = re.compile('[^A-Z]').sub('',ciphertext.upper())
    subsequences = getSubsequences(ciphertext,keylength)
    topIMC = [] # top IMC of subsequences 
    top10 = [] # top 10 potential keys
    for seq in subsequences:
        topIMC.append(calculateTopIMC(seq))
   
    # get the top k potential key letters for each in keyletter index use dictionary to store indices to try possible combinations later
    potentialKeyLetterDictList = []
    for potentialKeyLetter in topIMC:
        tempDict = {}
        for i in range(keylength):
            tempList = []
            for j in range(keylength):
                tempDict[j] = (potentialKeyLetter[j][0],potentialKeyLetter[j][1])
            tempList.append(tempDict)
        potentialKeyLetterDictList.append(tempList)    
    
    # create possoible combinations 
    numbersForCombinations = []
    for i in range(keylength):
        numbersForCombinations.append(i)
    combinations = itertools.combinations_with_replacement(numbersForCombinations,keylength)
   
    # try every possible combination of the letters and calcultae their IMC
    potentialKeysIMC = []
    checked = []
    for combination in combinations:
        for i in range(keylength):
            keyword = ''
            totalIMC = 0
            for j in range(keylength):
                keyword+= potentialKeyLetterDictList[j][0][combination[j]][0]
                totalIMC+= potentialKeyLetterDictList[j][0][combination[j]][1]
            if keyword not in checked:
                checked.append(keyword)
                potentialKeysIMC.append((keyword,totalIMC))
   
    # sort accored to their IMC and get top10 
    potentialKeysIMC = sorted(potentialKeysIMC,key = lambda x:x[1], reverse=True)
    top10 = []
    for i in range(10):
        top10.append(potentialKeysIMC[i][0])
    return top10


def ngramsFreqsFromFile(n:int):
    '''To get ngram frequency from wells.txt'''
    with open('wells.txt','r') as file:
        text = file.read()
    l = len(text) - n + 1
    nGramFreq = {}
    for i in range(l):
        ngram = text[i:i+n] # make the ngram 
        if ngram in nGramFreq: # do the counts 
            nGramFreq[ngram]+=1
        else:
            nGramFreq[ngram] = 1
    
    for ngram in nGramFreq: # get the relative frequency based on formula 
        nGramFreq[ngram] = nGramFreq[ngram]/l 
    return nGramFreq

def ngramsFreqsFromText(text,n:int):
    '''to ge ngram frequency from any text provided'''
    l = len(text) - n + 1
    nGramFreq = {}
    for i in range(l):
        ngram = text[i:i+n] # make the ngram 
        if ngram in nGramFreq: # do the counts 
            nGramFreq[ngram]+=1
        else:
            nGramFreq[ngram] = 1
    for ngram in nGramFreq: # get the relative frequency based on formula 
        nGramFreq[ngram] = nGramFreq[ngram]/l 
    return nGramFreq

def keyScore(decryptedText:str, n: int):
    '''to get the score of the key using it's decrypted text with and ngramFreqs from wells.txt'''
    score = 0
    freq = ngramsFreqsFromFile(n)
    decryptedFreq = ngramsFreqsFromText(decryptedText,n)
    for i in decryptedFreq:
        if i in freq:
            score += decryptedFreq[i] * freq[i]        
    return score


def hackVigenere(ciphertext: str):
    """
    return a string containing the key to the cipher
    """
    var = 5
    ciphertext = re.sub('[^A-Za-z]','',ciphertext).upper() #remove nonletters from the ciphertext 
    # get potential key lengths 
    potentialKeyLengths = a7.keyLengthIC(ciphertext,var)
    finalKeys = []
    # for each potential key length try potential keys and get score 
    for n in potentialKeyLengths:
        if n > 2:
            potentialKeys = vigenereKeySolver(ciphertext,n)
            for key in potentialKeys:
                decryptedText = decryptVigenere(ciphertext,key)
                newbest = keyScore(decryptedText,n)
                finalKeys.append((key,newbest))
        break
    finalKeys = sorted(finalKeys, key=lambda x:x[1],reverse=True)
    # finalKeys.sort(key=lambda x:x[1],reverse=True)
    finalKey = finalKeys[0][0]
    # print(finalKeys)
    # print(finalKey)
    # print (2.9137096156205135e-06) > (5.827419231241028e-07)
    return finalKey
    

def crackPassword():
    """
    hack password_protected.txt and write it to a new file
    """
    with open('password_protected.txt','r') as file:
        text = file.read()
    key = hackVigenere(text)
    plainText = decryptVigenere(text,key)
    
    with open('plaintext.txt','w') as file:
        file.write(plainText)



def test():
    # get subsequence test 
    ciphertext = "EFGHIJKLMNOP"
    # subseq = getSubsequences(ciphertext,4)
    # print(subseq)
    
    # get letter freq test
    # print(getLetterFrequency('THAT'))

    # getIMC Test
    # print(getIMC('THAT'))
    
    # decrypt test 
    # ciphertext = 'QSZI XS LM1KL KVSYRH'
    # print(decrypt(ciphertext,'E'))
   
    # vigenereKeySolver Tests
    # ciphertext = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSPMYKVQXJTDCIOMEEXDQVSRXLRLKZHOV"
    # best_keys = vigenereKeySolver(ciphertext, 5)
    # assert best_keys[0] == "EVERY"

    # ciphertext = "VYCFNWEBZGHKPWMMCIOGQDOSTKFTEOBPBDZGUFUWXBJVDXGONCWRTAGYMBXVGUCRBRGURWTHGEMJZVYRQTGCWXF"
    # best_keys = vigenereKeySolver(ciphertext, 6)
    # assert best_keys[0] == "CRYPTO"
    
    # # hackVigenere Tests
    ciphertext = "ANNMTVOAZPQYYPGYEZQPFEXMUFITOCZISINELOSGMMOAETIKDQGSYXTUTKIYUSKWYXATLCBLGGHGLLWZPEYXKFELIEUNMKJMLRMPSEYIPPOHAVMCRMUQVKTAZKKXVSOOVIEHKKNUMHMFYOAVVMITACZDIZQESKLHARKAVEUTBKXSNMHUNGTNKRKIETEJBJQGGZFQNUNFDEGUU"
    key = hackVigenere(ciphertext)
    assert key == "MAGIC"

    ciphertext = "AQNRXXXSTNSKCEPUQRUETZWGLAQIOBFKUFMGWIFKSYARFJSFWSPVXHLEMVQXLSYFVDVMPFWTMVUSIVSQGVBMAREKEOWVACSGYXKDITYSKTEGLINCMMKLKDFRLLGNERZIUGITCWJVGHMPFEXLDIGGFXUEWJIHXXJVRHAWGFYMKMFVLBKAKEHHO"
    key = hackVigenere(ciphertext)
    assert key == "SECRET"

    ciphertext = "JDMJBQQHSEZNYAGVHDUJKCBQXPIOMUYPLEHQFWGVLRXWXZTKHWRUHKBUXPIGDCKFHBZKFZYWEQAVKCQXPVMMIKPMXRXEWFGCJDIIXQJKJKAGIPIOMRXWXZTKJUTZGEYOKFBLWPSSXLEJWVGQUOSUHLEPFFMFUNVVTBYJKZMUXARNBJBUSLZCJXETDFEIIJTGTPLVFMJDIIPFUJWTAMEHWKTPJOEXTGDSMCEUUOXZEJXWZVXLEQKYMGCAXFPYJYLKACIPEILKOLIKWMWXSLZFJWRVPRUHIMBQYKRUNPYJKTAPYOXDTQ"
    key = hackVigenere(ciphertext)
    assert key == "QWERTY"


    # crackPassword()

if __name__ == '__main__' and not flags.interactive:
    test()