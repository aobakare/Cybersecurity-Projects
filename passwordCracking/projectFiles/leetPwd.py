#OPTION 1 IS THE CORRECT LEET CONVERSION
import sys

file = open(sys.argv[1],"r")
wordList = []
for line in file:
    wordList.append(line.strip())


#print(wordList)

def convertToLeet1(char):
    result = char
    if char=='a':
        result = '4'
    elif char == 'b':
        result = '8'
    elif char == 'c':
        result = '<'
    elif char == 'e':
        result = '3'
    elif char == 'f':
        result = '7'
    elif char == 'g':
        result = '6'
    elif char == 'h':
        result = '#'
    elif char == 'i':
        result = '1'
    elif char == 'j':
        result = '9'
    elif char == 'l':
        result = '1'
    elif char == 'o':
        result = '0'
    elif char == 'q':
        result = '0'
    elif char == 's':
        result = '5'
    elif char == 't':
        result = '7'
    elif char == 'x':
        result = '%'
    elif char == 'z':
        result = '2'
    return result

def convertToLeet2(char):
    result = char
    if char=='a':
        result = '@'
    elif char == 'b':
        result = '6'
    elif char == 'c':
        result = '<'
    elif char == 'e':
        result = '3'
    elif char == 'f':
        result = '7'
    elif char == 'g':
        result = '-'
    elif char == 'h':
        result = '#'
    elif char == 'i':
        result = '!'
    elif char == 'j':
        result = '9'
    elif char == 'l':
        result = '|'
    elif char == 'o':
        result = '0'
    elif char == 'q':
        result = '9'
    elif char == 's':
        result = '$'
    elif char == 't':
        result = '+'
    elif char == 'x':
        result = '*'
    elif char == 'z':
        result = '5'
    return result

def convertToLeet3(char):
    result = char
    if char=='a':
        result = '4'
    elif char == 'b':
        result = '8'
    elif char == 'c':
        result = '<'
    elif char == 'e':
        result = '3'
    elif char == 'f':
        result = '7'
    elif char == 'g':
        result = '6'
    elif char == 'h':
        result = '#'
    elif char == 'i':
        result = '9'
    elif char == 'j':
        result = '9'
    elif char == 'l':
        result = '1'
    elif char == 'o':
        result = '0'
    elif char == 'q':
        result = '0'
    elif char == 's':
        result = '5'
    elif char == 't':
        result = '7'
    elif char == 'x':
        result = '%'
    elif char == 'z':
        result = '2'
    return result

def convertToLeet4(char):
    result = char
    if char=='a':
        result = '4'
    elif char == 'b':
        result = '8'
    elif char == 'c':
        result = '<'
    elif char == 'e':
        result = '3'
    elif char == 'f':
        result = '7'
    elif char == 'g':
        result = '6'
    elif char == 'h':
        result = '#'
    elif char == 'i':
        result = '|'
    elif char == 'j':
        result = '9'
    elif char == 'l':
        result = '1'
    elif char == 'o':
        result = '0'
    elif char == 'q':
        result = '0'
    elif char == 's':
        result = '5'
    elif char == 't':
        result = '7'
    elif char == 'x':
        result = '%'
    elif char == 'z':
        result = '2'
    return result


mangle = list(wordList[4])
print(mangle)


newFile = open('leetOption1','w')
#This will convert each two different characters of each word
for word in wordList:
    for i in range(len(word)):
        temp = list(word)
        nxt = i+1
        temp[i] = convertToLeet1(temp[i])
        while (nxt < len(word)):
            temp2 = list(temp)
            temp2[nxt] = convertToLeet1(temp2[nxt])
            w = "".join(temp2)
            newFile.write(w)
            newFile.write('\n')
            #print(w)
            nxt += 1

file.close()
newFile.close()
