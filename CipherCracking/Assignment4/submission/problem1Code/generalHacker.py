# Affine and Transposition Cipher Hacker
# http://inventwithpython.com/hacking (BSD Licensed)

import os, sys, util, detectEnglish, cryptomath, caesar, transposition
import itertools 
import assign4_affine as affine


def hack(ciphertext): # CHANGE TO TRY ALL CIPHERS AND ALL POSSIBLE KEYS 
    cipherTypes = ['caesar','transposition','affine']
    for cipherType in cipherTypes:
        if cipherType == 'caesar':
            keyRange = getTextFromFile("dictionary.txt")
            for key in keyRange:
                decrypted = caesar.decrypt(ciphertext,key)
                if detectEnglish.isEnglish(decrypted):
                    print('Key %s: %s' % (key, decrypted[:200]))
                    return decrypted          
        elif cipherType == 'transposition':
            keyRange = []
            numbers = [1]
            for i in range(2,10):  
                numbers.append(i) # add col numbers incrementally
                keyRange= list(itertools.permutations(numbers)) # get permutations of the col numbers
                for key in keyRange: # for each permutation try to decrypt
                    decrypted = transposition.decryptMessage(key, ciphertext)
                    if detectEnglish.isEnglish(decrypted):
                        print('Key %s: %s' % (key, decrypted[:200]))
                        return decrypted
        elif cipherType == 'affine':
            keyRange = range(len(affine.SYMBOLS) ** 2)
            for key in keyRange:
                keyA = affine.getKeyParts(key)[0]
                if cryptomath.gcd(keyA, len(affine.SYMBOLS)) != 1:
                    continue
                decrypted = affine.affine(key, ciphertext)
                if detectEnglish.isEnglish(decrypted):
                    print('Key %s: %s' % (key, decrypted[:200]))
                    return decrypted
    return None

def getTextFromFile(filename): # GET EACH LINE IN THE TEXT FILE and put them in a list 
    if not os.path.exists(filename):
        print('The file %s does not exist' % (filename))
        sys.exit()
    
    lines = []
    fileObj = open(filename,'r')
    for line in fileObj:
        lines.append(line.strip())
    fileObj.close()
    return lines


def main():
    ciphertext = getTextFromFile('ciphers_version2.txt')
    ciphertext[3] = ciphertext[3].rjust(len(ciphertext[3])+1, ' ')
    outputFile = open('a4.txt','w')
    # print(ciphertext[3])
    for line in range(len(ciphertext)): # FOR EACH LINE IN THE cipherText Hack
        print("Line", str(line+1))
        hackedMessage = hack(ciphertext[line])
        outputFile.write(hackedMessage)
        outputFile.write('\n')
        # NEED TO WRITE TO A TEXT FILE 
        if hackedMessage == None:
            print('Failed to hack encryption.')

    outputFile.close()
        

if __name__ == '__main__':
    main()