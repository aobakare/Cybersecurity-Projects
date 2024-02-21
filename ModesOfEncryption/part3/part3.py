import random
import string

def generateRepeatedChar(x):
    rand = ""
    for i in range(0,x):
        rand += random.choice(string.ascii_letters)
    rand = rand * 50
    return rand

def generateRand(x):
    rand = ""
    for i in range(0,x):
        rand += random.choice(string.ascii_letters)

    return rand

file1char = generateRepeatedChar(8)
file2char= generateRepeatedChar(12)
file3char = generateRand(600)



y = "fileAXYZerrorsalted.enc"
def changeSingleByte(file):
    errorFile = open(file,"rb")
    errorFileList = list(errorFile.read())
    mid = int(len(errorFileList)/2)
    errorFileList[mid] = 64
    byteArray = bytearray(errorFileList)
    errorFile.close()
    return byteArray

# fileErrorBytearray = changeSingleByte("file3ofbsalted.enc")
#
# fileError = open("file3ofberrorsalted.enc","wb")
# fileError.write(fileErrorBytearray)
# fileError.close()











ciphertext3File = open("ciphertext3", "rb")
cText = list(ciphertext3File.read())
cTextHex = []
for x in cText:
        y = hex(x)
        cTextHex.append(y)

cTextEachLine = [] #THIS WILL HOLD EACH LINE WHICH IS 32 BYTES
count = 0
for x in range(0,len(cText),32):#jump by 32
    if x == len(cText) - 16: #this will neglect the padding which is the last 16 bytes
        break
    line = [] # to hold each 32bytes
    for y in range(x,x+32): #from current 32bytes to next 32 bytes
        line.append(cTextHex[y])
    cTextEachLine.append(line)

cTextEachLineSplit = [] #THIS WILL HOLD EACH LINE SPLIT INTO 1ST 16 AND 2ND 16
for x in range(len(cTextEachLine)):
    firstSplit = []
    secondSplit = []
    container = [] #this will hold the first split(16bytes) and second split(16bytes) of each line
    for y in range(0,16): #this will add the first 16
        firstSplit.append(cTextEachLine[x][y])
    for y in range(16,32): #this will add the second 16
        secondSplit.append(cTextEachLine[x][y])
    container.append(firstSplit)
    container.append(secondSplit)
    cTextEachLineSplit.append(container)

same = 0
sameList = []
diff = 0
diffList = []

#TO GET ALL THE SALARIES WHICH IS EVERY SECOND ELEMENT IN cTextEachLineSplit
salariesByline = []
for line in cTextEachLineSplit:
    #print(line)
    #print(len(line))
    salariesByline.append(line[1])


#TO GET THE SAME SALARIES AND DIFFERENT ONES
for i in range(len(salariesByline)):
    check = salariesByline[i] #current salary line
    j = i+1 #next salary line
    diffList.append(j) #assume all lines are different until we check
    for x in range(j,len(salariesByline)):
        lineNo = x + 1
        if check == salariesByline[x]:
            if (j) not in sameList:
                same = same +1
                sameList.append(j)
            if lineNo not in sameList:
                same = same+1
                sameList.append(lineNo)
        else:
            if j in sameList: #if j already  in sameList we remove it
                try:
                    diffList.remove(j)
                except ValueError:
                    pass



print("no same lines = " + str(same))
print(sameList)
print("no diff lines = " + str(len(diffList)))
print(diffList)

#TO EXCHANGE LINE 3 AND 4
modifiedFileList = cTextEachLineSplit.copy()
temp = modifiedFileList[2][1] # (line 3 is index 2) store in a temporary variable
modifiedFileList[2][1] = modifiedFileList[3][1] # (line 4 is index 3) set line 3 to line 4
modifiedFileList[3][1] = temp # set line 4 to temp( which holds line 3)

#UNSPLIT THE LIST BACK INTO ONE ARRAY FOR READING PURPOSES
accModFiletoRead = [] #will hold the list of all 496 bytes with the line change
count = 0
for x in range(len(modifiedFileList)):#unsplit the list into one long array of 496 bytes
    for y in range(len(modifiedFileList[x])):
        for z in modifiedFileList[x][y]:
            accModFiletoRead.append(z)

#TO ADD THE PADDING
lenghtWithoutPadding =  len(accModFiletoRead)
lenghtWithPadding = lenghtWithoutPadding + 16
for x in range(lenghtWithoutPadding,lenghtWithPadding):
    #print(x)
    accModFiletoRead.append(cTextHex[x])

#Read into New modified cipherText3 file
def covertTobyteArray(list): #function to convert list of hex to writeable format
    newList = []
    for x in list: #convert back to binary
        y = int(x,16)
        newList.append(y)
    barray = bytearray(newList)
    return barray
bArray = covertTobyteArray(accModFiletoRead) #convert to binary format
#READ TO MODIFIED FILE
#cfile = open("ciphertext3.mod","wb")
#cfile.write(bArray)
#cfile.close()




