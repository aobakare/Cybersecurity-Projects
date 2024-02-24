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
Enhanced substitution cipher solver.
"""

import re, simpleSubHacker, util

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def hackSimpleSub(message: str):
    """
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.
    """
    messagelist = message.split()
    letterMapping =  simpleSubHacker.hackSimpleSub(message) # to get the letter mapping 
    initialDicpher = simpleSubHacker.decryptWithCipherletterMapping(message, letterMapping)
    initialDicpherList  = initialDicpher.split() # list of all words from the first pass with partial words
    partialWords = [] # list of all partial words from the initial pass
    partialWordsCiphertext = [] # the partial words corresponding ciphertext 
    
    # get all partial words and their corresponding ciphertext (both indices will match), with any punc
    for i in range(len(initialDicpherList)): 
        if '_' in initialDicpherList[i]:
            partialWords.append(removePunctuations(initialDicpherList[i]).upper())
            partialWordsCiphertext.append(removePunctuations(messagelist[i]).upper())
    
    # create pattern for each patial word and get all their matches into a list 
    fill = '[a-z]'
    matches = [] # list of all matches in the dictionary (indices will also match the above)
    for word in partialWords: 
        pattern = '' # we need to create the regex pattern
        for letter in word: 
            if letter != '_':
                pattern += letter.upper()
            else:
                pattern+=fill
        pattern+='$'
        matches.append(util.checkWord(pattern))

    # reducing multiple mappings
    for i in range(len(partialWordsCiphertext)):
        if len(matches[i]) == 1 and partialWords[i].count('_') == 1 : # if it only has one match and one letter missing then it has to be that word(letter)
            letterIndex = partialWords[i].index('_') # get the index of the _
            wordMatch = matches[i][0]
            letterMapping[partialWordsCiphertext[i][letterIndex]] = [wordMatch[letterIndex]] # set the letter to its match in letter mapping
            letterMapping = simpleSubHacker.removeSolvedLettersFromMapping(letterMapping) # remove these solved from the mapping 
    
    fullDicipher = ['' for i in range(len(messagelist))]
    done = False 
    while not done:
        for i in range(len(initialDicpherList)): # for each word in initial dicphiered message 
            if '_' in initialDicpherList[i] : # if underscore present 
                for index in range(len(initialDicpherList[i])): # for each charcter in that word 
                    if initialDicpherList[i][index] == '_': # if that character index is the underscore
                        cipherTextLetter  = messagelist[i][index] # get the corresponding cipherText letter in original cipher text 
                        CipherTextMap = letterMapping[cipherTextLetter.upper()] # get the plaintext letter it maps to 
                        if len(CipherTextMap) == 1: # if that cipher text letter map has a len 1 then it has been accurately mapped
                            whatCase = checkCase(cipherTextLetter) # check casing to be accurate 
                            # fill in the underscore in correct casing 
                            if whatCase == 'lowercase':
                                initialDicpherList[i] = replaceChar(initialDicpherList[i],index,CipherTextMap[0].lower()) 
                            else:
                                initialDicpherList[i] = replaceChar(initialDicpherList[i],index,CipherTextMap[0].upper())
                        elif len(CipherTextMap)>1: # that cipher text letter has not been accurately mapped
                            matches = getMatches(initialDicpherList[i])
                            if len(matches) == 1: # it has to be that word
                                matchLetter = matches[0][0][index]
                                for mapLetter in CipherTextMap:
                                    if mapLetter == matchLetter:
                                        letterMapping[cipherTextLetter.upper()] =  [matchLetter]
                                        letterMapping = simpleSubHacker.removeSolvedLettersFromMapping(letterMapping) # remove these solved from the mapping
                                        CipherTextMap = letterMapping[cipherTextLetter.upper()] # get the plaintext letter it maps to
                                        whatCase = checkCase(cipherTextLetter) # check casing to be accurate 
                                        if whatCase == 'lowercase':
                                            initialDicpherList[i] = replaceChar(initialDicpherList[i],index,CipherTextMap[0].lower())
                                        else:
                                            initialDicpherList[i] = replaceChar(initialDicpherList[i],index,CipherTextMap[0].upper())
                fullDicipher[i] = initialDicpherList[i] # add to fullDicipher    
            else: # nothing to do just add it 
               fullDicipher[i] = initialDicpherList[i] # add to fullDicipher
        for i in range(len(fullDicipher)):
            if '_' in fullDicipher[i]: # we are done replacing all partial words
                matches = getMatches(initialDicpherList[i])[0]
                index = fullDicipher[i].index('_')
                cipherTextLetter = messagelist[i][index]
                mapped = list(letterMapping.values())
                accMap = []
                for map in mapped: # get already mapped
                    if len(map) == 1:
                        accMap.append(map)
                for match in matches: # for each match 
                    if [match[index]] not in accMap: # not mapped already 
                            letterMapping[cipherTextLetter.upper()] = [match[index]]
                            letterMapping = simpleSubHacker.removeSolvedLettersFromMapping(letterMapping) # remove these solved from the mapping
                CipherTextMap = letterMapping[cipherTextLetter.upper()]
                whatCase = checkCase(cipherTextLetter) # check casing to be accurate 
                if whatCase == 'lowercase':
                    fullDicipher[i] = replaceChar(fullDicipher[i],index,CipherTextMap[0].lower())
                else:
                    fullDicipher[i] = replaceChar(fullDicipher[i],index,CipherTextMap[0].upper())
            else:
                done = True
    fullDicipher = ' '.join(fullDicipher)
    return fullDicipher
            
    
   
# function to remove punctuations from word
def removePunctuations(word:str):  
    pattern = r'[^\w\s]' # not word character (letter, digit or underscore) or space
    newWord= re.sub(pattern, '', word)
    return newWord

# function to replace a charcater in a specific index 
def replaceChar(inputString, index, replacementChar):
    # Convert the input string to a list of characters
    stringList = list(inputString)
    # Replace the character at the specified index with the replacement character
    stringList[index] = replacementChar
    
    # Convert the list back to a string
    replacedString = ''.join(stringList)
    return replacedString

# function to check case of a string 
def checkCase(char):
    if char.isupper():
        return "uppercase"
    elif char.islower():
        return "lowercase"
# function to get matches for partial words   
def getMatches(word):
    fill = '[a-z]'
    matches = [] # list of all matches in the dictionary (indices will also match the above)
    pattern = '' # we need to create the regex pattern
    for letter in word: 
        if letter != '_':
            pattern += letter.upper()
        else:
            pattern+=fill
    pattern+='$'
    matches.append(util.checkWord(pattern))
    return matches


def test():
    # Provided test.
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    print(hackSimpleSub(message))
    # End of provided test.
    

if __name__ == '__main__':
    test()

