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
Assignment 10
"""
from sys import flags
import os
import time

def getSSD(text:str):
    '''To calculate the SSD of a text'''
    text = text.upper()
    freq={}
    SSD = []
    lenOfText = 0
    for letter in text:
        if letter.isalpha(): 
            lenOfText+=1 # increment to get the actual len for ssd calculation 
            if letter not in freq: # add letter to dictionary if not already in 
                freq[letter] = 0
            freq[letter]+=1 # increase freq of that letter    

    # freq = Counter(filter(str.isalpha, text))
    # make the key,value into a list of lists so it can be easily sorted 
    for key in freq.keys(): 
        SSD.append([key,freq[key]])
    # sort frew distribution 
    SSD.sort(key= lambda x:x[1], reverse=True)
    # calculate relative frequencies 
    for item in SSD:
        item[1] = item[1]/lenOfText
    # print(SSD)
    return SSD

def getDistance(p1:list, p2:list):
    '''To get distance between p1 and p1. Note: p1 = cipherTextSSD and p2 = textSSD'''
    p1Len = len(p1) 
    p2Len = len(p2)
    alpaLen = max(p1Len,p2Len) # total alphabet len would be largest of the 2
    distance = 0
    for i in range(alpaLen):
        # assign p as 0 for unseen ranks 
        if i >= p1Len:
            p1Number = 0
        else:
            p1Number = p1[i][1]
        if i >= p2Len:
            p2Number = 0
        else: 
            p2Number = p2[i][1]
        #calculate according to formula
        distance += (p1Number-p2Number)**2
    return float(distance)

def cliSSD(ciphertext:str, files:list):
    """
    Args:
        ciphertext (str)
        files (list of str)
    Returns:
        dict
    """
    distanceDict = {}
    cipherTextSSD = getSSD(ciphertext) # get cipherTextSSD
    for fileName in files:
        # file = open(fileName,'r',encoding='utf8')
        with open(fileName,'r',encoding='utf8') as file:
            text = file.read()
        textSSD = getSSD(text) # get textSSD
        distance = getDistance(cipherTextSSD,textSSD) # get distance between cipherTextSSD and textSSD
        distanceDict[fileName] = distance
    
    return distanceDict

def getDPD(text:str):
    text = text.upper().split() # convert text to upper case and group words
    DPDlist = []
    for word in text: # for each word
        DPDtuple = []
        freq={}
        for letter in word: 
            if letter.isalpha():
                if letter not in freq: # add letter to dictionary if not already in 
                    freq[letter] = 0
                freq[letter]+=1 # increase freq of that letter    
        
        for key in freq.keys(): # get the freq distribution for each distint letter 
            DPDtuple.append(freq[key])
        
        DPDtuple.sort(reverse=True)  
        DPDlist.append(tuple(DPDtuple))
    DPD = {}
    DPDlen = len(DPDlist) # total number of DPDs
    # to count the freq of DPDs
    for item in DPDlist:
        if item not in DPD:
            DPD[item] = 0
        DPD[item]+=1
    # calculate relative frequencies 
    for key in DPD.keys():
        DPD[key] = float(DPD[key]/DPDlen)
    # print(DPD)
    return DPD

def getDPDDistance(p1:dict, p2:dict):
    p1Keys = list(p1.keys())
    p2Keys = list(p2.keys())
    totalKeys = list(set(p1Keys+p2Keys))
    distance = 0
    for key in totalKeys:
        # assign p as 0 for unseen ranks 
        if key not in p1Keys:
            p1Number = 0
        else:
            p1Number = p1[key]
        if key not in p2Keys:
            p2Number = 0
        else: 
            p2Number = p2[key]
        #calculate according to formula
        distance += (p1Number-p2Number)**2

    return float(distance)

def cliDPD(ciphertext: str, files):
    """
    Args:
        ciphertext (str)
        files (list of str)
    Returns:
        dict
    """
    distanceDict = {}
    cipherTextSSD = getDPD(ciphertext) # get cipherTextSSD
    for fileName in files:
        # file = open(fileName,'r',encoding='utf8')
        with open(fileName,'r',encoding='utf8') as file:
            text = file.read()
        textSSD = getDPD(text) # get textSSD
        distance = getDPDDistance(cipherTextSSD,textSSD) # get distance between cipherTextSSD and textSSD
        distanceDict[fileName] = distance
    
    return distanceDict

def cliSSDTest(ciphertext_files, sampletext_files):
    """
    Args:
        ciphertext_files (list of str)
        sampletext_files (list of str)
    Returns:
        dict
    """
    SSD =  {}
    for ciphertext in ciphertext_files:
        # file = open(ciphertext,'r',encoding='utf8')
        with open(ciphertext,'r',encoding='utf8') as file:
            text = file.read()
        # cipherSSD = getSSD(text)
        distances=cliSSD(text,sampletext_files)
        distanceList = []
        for key in distances.keys():
            distanceList.append((key,distances[key]))
        distanceList.sort(key = lambda x:x[1])
        SSD[ciphertext] = distanceList[0][0]
        SSD = dict(sorted(SSD.items()))
    return SSD

def cliDPDTest(ciphertext_files, sampletext_files):
    """
    Args:
        ciphertext_files (list of str)
        sampletext_files (list of str)
    Returns:
        dict
    """
    DPD =  {}
    for ciphertext in ciphertext_files:
        # file = open(ciphertext,'r',encoding='utf8')
        with open(ciphertext,'r',encoding='utf8') as file:
            text = file.read()
        distances=cliDPD(text,sampletext_files)
        distanceList = []
        for key in distances.keys():
            distanceList.append((key,distances[key]))
        distanceList.sort(key = lambda x:x[1])
        DPD[ciphertext] = distanceList[0][0]
        DPD = dict(sorted(DPD.items()))
    return DPD

def getMatrix(SSD:dict):
    languages = ['bg','nl','en','fr','de','el','it','pl','ru','es']
    SSDlist = []
    for key in SSD.keys():
        ssd = [key.split('_')[1], SSD[key].split('_')[1]]
        SSDlist.append(ssd)
    # print(SSDlist)
    matrix = []
    
    for lang in languages:
        row = []
        row.append(lang) #to know the language we are checking
        bg= 0
        de=0
        el=0
        en=0
        es=0
        fr=0
        it=0
        nl=0
        pl=0
        ru=0
        for ssd in SSDlist:
            if lang == ssd[0]: # if language is the ciphertext file
                if ssd[1] == 'bg.txt':
                    bg+=1
                elif ssd[1] == 'de.txt':
                    de+=1
                elif ssd[1] == 'el.txt':
                    el+=1
                elif ssd[1] == 'en.txt':
                    en+=1
                elif ssd[1] == 'es.txt':
                    es+=1
                elif ssd[1] == 'fr.txt':
                    fr+=1
                elif ssd[1] == 'it.txt':
                    it+=1
                elif ssd[1] == 'nl.txt':
                    nl+=1
                elif ssd[1] == 'pl.txt':
                    pl+=1
                elif ssd[1] == 'ru.txt':
                    ru+=1
        row.append(['bg',bg])
        row.append(['nl',nl])
        row.append(['en',en])
        row.append(['fr',fr])
        row.append(['de',de])
        row.append(['el',el])
        row.append(['it',it])
        row.append(['pl',pl])
        row.append(['ru',ru])
        row.append(['es',es])
        matrix.append(row)
    return matrix

def test():
    # to get list of files in that directory 
    # arr = os.listdir("/Users/abdulb/Desktop/CMPUT331/Assignment10")
    # cipherFiles = []
    # sampleFiles = []
    # for file in arr:
    #     if 'cipher' in file:
    #         cipherFiles.append(file)
    #     elif 'sample' in file:
    #         sampleFiles.append(file)
    
    # ciphertext = "abcdefghijklmnopqrstuvwxyz"
    # distanceDict = cliSSD(ciphertext,sampleFiles)
    # print(distanceDict)
    # print(cipherFiles)
    # print(sampleFiles)

    # start_time = time.time()
    # with open('SSD.txt','w') as file:
    #     SSD = cliSSDTest(cipherFiles,sampleFiles)
    #     file.write(str(SSD))
    # with open('DPD.txt','w') as file:
    #     DPD = cliDPDTest(cipherFiles,sampleFiles)
    #     file.write(str(DPD))
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(elapsed_time)

    SSD = {'ciphertext_bg_1.txt': 'sample_bg.txt', 'ciphertext_bg_2.txt': 'sample_bg.txt', 'ciphertext_bg_3.txt': 'sample_bg.txt', 'ciphertext_bg_4.txt': 'sample_bg.txt', 'ciphertext_bg_5.txt': 'sample_ru.txt', 'ciphertext_bg_6.txt': 'sample_ru.txt', 'ciphertext_bg_7.txt': 'sample_bg.txt', 'ciphertext_bg_8.txt': 'sample_bg.txt', 'ciphertext_bg_9.txt': 'sample_bg.txt', 'ciphertext_de_1.txt': 'sample_de.txt', 'ciphertext_de_2.txt': 'sample_de.txt', 'ciphertext_de_3.txt': 'sample_de.txt', 'ciphertext_de_4.txt': 'sample_en.txt', 'ciphertext_de_5.txt': 'sample_de.txt', 'ciphertext_de_6.txt': 'sample_nl.txt', 'ciphertext_de_7.txt': 'sample_de.txt', 'ciphertext_de_8.txt': 'sample_de.txt', 'ciphertext_de_9.txt': 'sample_de.txt', 'ciphertext_el_1.txt': 'sample_el.txt', 'ciphertext_el_2.txt': 'sample_el.txt', 'ciphertext_el_3.txt': 'sample_el.txt', 'ciphertext_el_4.txt': 'sample_ru.txt', 'ciphertext_el_5.txt': 'sample_el.txt', 'ciphertext_el_6.txt': 'sample_el.txt', 'ciphertext_el_7.txt': 'sample_el.txt', 'ciphertext_el_8.txt': 'sample_el.txt', 'ciphertext_el_9.txt': 'sample_el.txt', 'ciphertext_en_1.txt': 'sample_it.txt', 'ciphertext_en_2.txt': 'sample_bg.txt', 'ciphertext_en_3.txt': 'sample_en.txt', 'ciphertext_en_4.txt': 'sample_es.txt', 'ciphertext_en_5.txt': 'sample_it.txt', 'ciphertext_en_6.txt': 'sample_en.txt', 'ciphertext_en_7.txt': 'sample_en.txt', 'ciphertext_en_8.txt': 'sample_en.txt', 'ciphertext_en_9.txt': 'sample_en.txt', 'ciphertext_es_1.txt': 'sample_it.txt', 'ciphertext_es_2.txt': 'sample_es.txt', 'ciphertext_es_3.txt': 'sample_es.txt', 'ciphertext_es_4.txt': 'sample_fr.txt', 'ciphertext_es_5.txt': 'sample_es.txt', 'ciphertext_es_6.txt': 'sample_es.txt', 'ciphertext_es_7.txt': 'sample_es.txt', 'ciphertext_es_8.txt': 'sample_es.txt', 'ciphertext_es_9.txt': 'sample_es.txt', 'ciphertext_fr_1.txt': 'sample_fr.txt', 'ciphertext_fr_2.txt': 'sample_fr.txt', 'ciphertext_fr_3.txt': 'sample_fr.txt', 'ciphertext_fr_4.txt': 'sample_fr.txt', 'ciphertext_fr_5.txt': 'sample_fr.txt', 'ciphertext_fr_6.txt': 'sample_es.txt', 'ciphertext_fr_7.txt': 'sample_fr.txt', 'ciphertext_fr_8.txt': 'sample_fr.txt', 'ciphertext_fr_9.txt': 'sample_fr.txt', 'ciphertext_it_1.txt': 'sample_it.txt', 'ciphertext_it_2.txt': 'sample_it.txt', 'ciphertext_it_3.txt': 'sample_it.txt', 'ciphertext_it_4.txt': 'sample_it.txt', 'ciphertext_it_5.txt': 'sample_it.txt', 'ciphertext_it_6.txt': 'sample_it.txt', 'ciphertext_it_7.txt': 'sample_it.txt', 'ciphertext_it_8.txt': 'sample_it.txt', 'ciphertext_it_9.txt': 'sample_it.txt', 'ciphertext_nl_1.txt': 'sample_nl.txt', 'ciphertext_nl_2.txt': 'sample_nl.txt', 'ciphertext_nl_3.txt': 'sample_nl.txt', 'ciphertext_nl_4.txt': 'sample_nl.txt', 'ciphertext_nl_5.txt': 'sample_nl.txt', 'ciphertext_nl_6.txt': 'sample_nl.txt', 'ciphertext_nl_7.txt': 'sample_nl.txt', 'ciphertext_nl_8.txt': 'sample_nl.txt', 'ciphertext_nl_9.txt': 'sample_nl.txt', 'ciphertext_pl_1.txt': 'sample_pl.txt', 'ciphertext_pl_2.txt': 'sample_pl.txt', 'ciphertext_pl_3.txt': 'sample_pl.txt', 'ciphertext_pl_4.txt': 'sample_pl.txt', 'ciphertext_pl_5.txt': 'sample_pl.txt', 'ciphertext_pl_6.txt': 'sample_pl.txt', 'ciphertext_pl_7.txt': 'sample_pl.txt', 'ciphertext_pl_8.txt': 'sample_pl.txt', 'ciphertext_pl_9.txt': 'sample_pl.txt', 'ciphertext_ru_1.txt': 'sample_ru.txt', 'ciphertext_ru_2.txt': 'sample_ru.txt', 'ciphertext_ru_3.txt': 'sample_ru.txt', 'ciphertext_ru_4.txt': 'sample_ru.txt', 'ciphertext_ru_5.txt': 'sample_ru.txt', 'ciphertext_ru_6.txt': 'sample_ru.txt', 'ciphertext_ru_7.txt': 'sample_en.txt', 'ciphertext_ru_8.txt': 'sample_ru.txt', 'ciphertext_ru_9.txt': 'sample_ru.txt'}
    DPD = {'ciphertext_bg_1.txt': 'sample_bg.txt', 'ciphertext_bg_2.txt': 'sample_bg.txt', 'ciphertext_bg_3.txt': 'sample_bg.txt', 'ciphertext_bg_4.txt': 'sample_bg.txt', 'ciphertext_bg_5.txt': 'sample_bg.txt', 'ciphertext_bg_6.txt': 'sample_bg.txt', 'ciphertext_bg_7.txt': 'sample_bg.txt', 'ciphertext_bg_8.txt': 'sample_bg.txt', 'ciphertext_bg_9.txt': 'sample_bg.txt', 'ciphertext_de_1.txt': 'sample_de.txt', 'ciphertext_de_2.txt': 'sample_de.txt', 'ciphertext_de_3.txt': 'sample_de.txt', 'ciphertext_de_4.txt': 'sample_de.txt', 'ciphertext_de_5.txt': 'sample_de.txt', 'ciphertext_de_6.txt': 'sample_de.txt', 'ciphertext_de_7.txt': 'sample_de.txt', 'ciphertext_de_8.txt': 'sample_de.txt', 'ciphertext_de_9.txt': 'sample_de.txt', 'ciphertext_el_1.txt': 'sample_el.txt', 'ciphertext_el_2.txt': 'sample_el.txt', 'ciphertext_el_3.txt': 'sample_el.txt', 'ciphertext_el_4.txt': 'sample_el.txt', 'ciphertext_el_5.txt': 'sample_el.txt', 'ciphertext_el_6.txt': 'sample_el.txt', 'ciphertext_el_7.txt': 'sample_el.txt', 'ciphertext_el_8.txt': 'sample_el.txt', 'ciphertext_el_9.txt': 'sample_el.txt', 'ciphertext_en_1.txt': 'sample_en.txt', 'ciphertext_en_2.txt': 'sample_en.txt', 'ciphertext_en_3.txt': 'sample_en.txt', 'ciphertext_en_4.txt': 'sample_en.txt', 'ciphertext_en_5.txt': 'sample_en.txt', 'ciphertext_en_6.txt': 'sample_en.txt', 'ciphertext_en_7.txt': 'sample_en.txt', 'ciphertext_en_8.txt': 'sample_en.txt', 'ciphertext_en_9.txt': 'sample_nl.txt', 'ciphertext_es_1.txt': 'sample_es.txt', 'ciphertext_es_2.txt': 'sample_es.txt', 'ciphertext_es_3.txt': 'sample_es.txt', 'ciphertext_es_4.txt': 'sample_es.txt', 'ciphertext_es_5.txt': 'sample_es.txt', 'ciphertext_es_6.txt': 'sample_es.txt', 'ciphertext_es_7.txt': 'sample_es.txt', 'ciphertext_es_8.txt': 'sample_es.txt', 'ciphertext_es_9.txt': 'sample_es.txt', 'ciphertext_fr_1.txt': 'sample_fr.txt', 'ciphertext_fr_2.txt': 'sample_fr.txt', 'ciphertext_fr_3.txt': 'sample_fr.txt', 'ciphertext_fr_4.txt': 'sample_es.txt', 'ciphertext_fr_5.txt': 'sample_fr.txt', 'ciphertext_fr_6.txt': 'sample_fr.txt', 'ciphertext_fr_7.txt': 'sample_fr.txt', 'ciphertext_fr_8.txt': 'sample_fr.txt', 'ciphertext_fr_9.txt': 'sample_fr.txt', 'ciphertext_it_1.txt': 'sample_it.txt', 'ciphertext_it_2.txt': 'sample_it.txt', 'ciphertext_it_3.txt': 'sample_it.txt', 'ciphertext_it_4.txt': 'sample_it.txt', 'ciphertext_it_5.txt': 'sample_it.txt', 'ciphertext_it_6.txt': 'sample_it.txt', 'ciphertext_it_7.txt': 'sample_it.txt', 'ciphertext_it_8.txt': 'sample_it.txt', 'ciphertext_it_9.txt': 'sample_it.txt', 'ciphertext_nl_1.txt': 'sample_nl.txt', 'ciphertext_nl_2.txt': 'sample_nl.txt', 'ciphertext_nl_3.txt': 'sample_nl.txt', 'ciphertext_nl_4.txt': 'sample_nl.txt', 'ciphertext_nl_5.txt': 'sample_nl.txt', 'ciphertext_nl_6.txt': 'sample_nl.txt', 'ciphertext_nl_7.txt': 'sample_nl.txt', 'ciphertext_nl_8.txt': 'sample_nl.txt', 'ciphertext_nl_9.txt': 'sample_nl.txt', 'ciphertext_pl_1.txt': 'sample_pl.txt', 'ciphertext_pl_2.txt': 'sample_pl.txt', 'ciphertext_pl_3.txt': 'sample_pl.txt', 'ciphertext_pl_4.txt': 'sample_pl.txt', 'ciphertext_pl_5.txt': 'sample_pl.txt', 'ciphertext_pl_6.txt': 'sample_pl.txt', 'ciphertext_pl_7.txt': 'sample_pl.txt', 'ciphertext_pl_8.txt': 'sample_pl.txt', 'ciphertext_pl_9.txt': 'sample_pl.txt', 'ciphertext_ru_1.txt': 'sample_ru.txt', 'ciphertext_ru_2.txt': 'sample_ru.txt', 'ciphertext_ru_3.txt': 'sample_ru.txt', 'ciphertext_ru_4.txt': 'sample_ru.txt', 'ciphertext_ru_5.txt': 'sample_ru.txt', 'ciphertext_ru_6.txt': 'sample_ru.txt', 'ciphertext_ru_7.txt': 'sample_ru.txt', 'ciphertext_ru_8.txt': 'sample_ru.txt', 'ciphertext_ru_9.txt': 'sample_pl.txt'}
    # names = ['Bulgarian', 'Dutch', 'English', 'French', 'German', 'Greek', 'Italian', 'Polish', 'Russian', 'Spanish']
    languages = ['bg','nl','en','fr','de','el','it','pl','ru','es']
    '''
    bg : Bulgarian
    de : German
    el : Greek
    en : English
    es : Spanish
    fr : French
    it : Italian
    nl : Dutch
    pl : Polish
    ru : Russian
    '''
    # SSDmatrix = getMatrix(SSD)
    # for row in SSDmatrix:
    #     print(row)
    #     print(" ")
    # print('------------------------------')
    # DPDmatrix = getMatrix(DPD)
    # for row in DPDmatrix:
    #     print(row)
    #     print(" ")

if __name__ == "__main__" and not flags.interactive:
    test()