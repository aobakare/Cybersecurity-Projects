import sys
file = open(sys.argv[1],"r")
oilerList = []
for line in file:
    oilerList.append(line.strip())


file.close()
oilerSplitList = [] #first and last name separated
for name in oilerList:
    splitName = list(name.split(" "))
    oilerSplitList.append(splitName)


def allLower(name,option): #first and last name lowercase
    result = ""
    first = name[0]
    second = name[1]
    if (option == 1):
        result = first.lower()+"$"+second.lower()
    elif (option == 2):
        result = first.lower() + "%" + second.lower()
    elif (option == 3):
        result = first.lower() + "*" + second.lower()
    elif (option == 4):
        result = first.lower() + "_" + second.lower()
    return result

def allUpper(name,option): #first and last name uppercase
    result = ""
    first = name[0]
    second = name[1]
    if (option == 1):
        result = first.upper() +"$"+second.upper()
    elif (option == 2):
        result = first.upper() + "%" + second.upper()
    elif (option == 3):
        result = first.upper() + "*" + second.upper()
    elif (option == 4):
        result = first.upper() + "_" + second.upper()
    return result

def firstUpper(name,option): #first name uppercase and last name lowercase
    result = ""
    first = name[0]
    second = name[1]
    if (option == 1):
        result = first.upper() +"$"+second.lower()
    elif (option == 2):
        result = first.upper() + "%" + second.lower()
    elif (option == 3):
        result = first.upper() + "*" + second.lower()
    elif (option == 4):
        result = first.upper() + "_" + second.lower()
    return result

def firstLower(name,option): #first name lowercase and last name uppercase
    result = ""
    first = name[0]
    second = name[1]
    if (option == 1):
        result = first.lower() +"$"+second.upper()
    elif (option == 2):
        result = first.lower() + "%" + second.upper()
    elif (option == 3):
        result = first.lower() + "*" + second.upper()
    elif (option == 4):
        result = first.lower() + "_" + second.upper()
    return result

def both1LetterUpper(name,option): #first and last name 1st letters uppercase only
    result = ""
    first = name[0]
    second = name[1]
    if (option == 1):
        result = first.capitalize() +"$"+second.capitalize()
    elif (option == 2):
        result = first.capitalize() + "%" + second.capitalize()
    elif (option == 3):
        result = first.capitalize() + "*" + second.capitalize()
    elif (option == 4):
        result = first.capitalize() + "_" + second.capitalize()
    return result

def option6a(name,option): #first name 1st letter upper case only and last name lowercase
    result = ""
    first = name[0]
    second = name[1]
    if (option == 1):
        result = first.capitalize() +"$"+second.lower()
    elif (option == 2):
        result = first.capitalize() + "%" + second.lower()
    elif (option == 3):
        result = first.capitalize() + "*" + second.lower()
    elif (option == 4):
        result = first.capitalize() + "_" + second.lower()
    return result

def option6b(name,option): #first name 1st letter upper case only and last name uppercase
    result = ""
    first = name[0]
    second = name[1]
    if (option == 1):
        result = first.capitalize() +"$"+second.upper()
    elif (option == 2):
        result = first.capitalize() + "%" + second.upper()
    elif (option == 3):
        result = first.capitalize() + "*" + second.upper()
    elif (option == 4):
        result = first.capitalize() + "_" + second.upper()
    return result

def option7a(name,option): #first name lowercase and last name first letter uppercase only
    result = ""
    first = name[0]
    second = name[1]
    if (option == 1):
        result = first.lower() +"$"+second.capitalize()
    elif (option == 2):
        result = first.lower() + "%" + second.capitalize()
    elif (option == 3):
        result = first.lower() + "*" + second.capitalize()
    elif (option == 4):
        result = first.lower() + "_" + second.capitalize()
    return result

def option7b(name,option): #first name uppercase and last name first letter uppercase only
    result = ""
    first = name[0]
    second = name[1]
    if (option == 1):
        result = first.upper() +"$"+second.capitalize()
    elif (option == 2):
        result = first.upper() + "%" + second.capitalize()
    elif (option == 3):
        result = first.upper() + "*" + second.capitalize()
    elif (option == 4):
        result = first.upper() + "_" + second.capitalize()
    return result

mangledFile = open(sys.argv[2],"w")
for name in oilerSplitList:
    # MANGLE OPTION 1
    mangle1a= allLower(name,1)
    mangledFile.write(mangle1a)
    mangledFile.write("\n")

    mangle1b= allLower(name,2)
    mangledFile.write(mangle1b)
    mangledFile.write("\n")

    mangle1c= allLower(name,3)
    mangledFile.write(mangle1c)
    mangledFile.write("\n")

    mangle1d= allLower(name,4)
    mangledFile.write(mangle1d)
    mangledFile.write("\n")

    #MANGLE OPTION 2
    mangle2a = allUpper(name,1)
    mangledFile.write(mangle2a)
    mangledFile.write("\n")

    mangle2b = allUpper(name,2)
    mangledFile.write(mangle2b)
    mangledFile.write("\n")

    mangle2c = allUpper(name,3)
    mangledFile.write(mangle2c)
    mangledFile.write("\n")

    mangle2d = allUpper(name,4)
    mangledFile.write(mangle2d)
    mangledFile.write("\n")

    # MANGLE OPTION 3
    mangle3a = firstLower(name, 1)
    mangledFile.write(mangle3a)
    mangledFile.write("\n")

    mangle3b = firstLower(name, 2)
    mangledFile.write(mangle3b)
    mangledFile.write("\n")

    mangle3c = firstLower(name, 3)
    mangledFile.write(mangle3c)
    mangledFile.write("\n")

    mangle3d = firstLower(name, 4)
    mangledFile.write(mangle3d)
    mangledFile.write("\n")

    # MANGLE OPTION 4
    mangle4a = firstUpper(name, 1)
    mangledFile.write(mangle4a)
    mangledFile.write("\n")

    mangle4b = firstUpper(name, 2)
    mangledFile.write(mangle4b)
    mangledFile.write("\n")

    mangle4c = firstUpper(name,3)
    mangledFile.write(mangle4c)
    mangledFile.write("\n")

    mangle4d = firstUpper(name,4)
    mangledFile.write(mangle4d)
    mangledFile.write("\n")

    # MANGLE OPTION 5
    mangle5a = both1LetterUpper(name,1)
    mangledFile.write(mangle5a)
    mangledFile.write("\n")

    mangle5b = both1LetterUpper(name,2)
    mangledFile.write(mangle5b)
    mangledFile.write("\n")

    mangle5c = both1LetterUpper(name,3)
    mangledFile.write(mangle5c)
    mangledFile.write("\n")

    mangle5d = both1LetterUpper(name,4)
    mangledFile.write(mangle5d)
    mangledFile.write("\n")

    # MANGLE OPTION 6
    mangle6a = option6a(name, 1)
    mangledFile.write(mangle6a)
    mangledFile.write("\n")

    mangle6b = option6a(name, 2)
    mangledFile.write(mangle6b)
    mangledFile.write("\n")

    mangle6c = option6a(name, 3)
    mangledFile.write(mangle6c)
    mangledFile.write("\n")

    mangle6d = option6a(name, 4)
    mangledFile.write(mangle6d)
    mangledFile.write("\n")

    # MANGLE OPTION 7
    mangle7a = option6b(name, 1)
    mangledFile.write(mangle7a)
    mangledFile.write("\n")

    mangle7b = option6b(name, 2)
    mangledFile.write(mangle7b)
    mangledFile.write("\n")

    mangle7c = option6b(name, 3)
    mangledFile.write(mangle7c)
    mangledFile.write("\n")

    mangle7d = option6b(name, 4)
    mangledFile.write(mangle7d)
    mangledFile.write("\n")

    # MANGLE OPTION 8
    mangle8a = option7a(name, 1)
    mangledFile.write(mangle8a)
    mangledFile.write("\n")

    mangle8b = option7a(name, 2)
    mangledFile.write(mangle8b)
    mangledFile.write("\n")

    mangle8c = option7a(name, 3)
    mangledFile.write(mangle8c)
    mangledFile.write("\n")

    mangle8d = option7a(name, 4)
    mangledFile.write(mangle8d)
    mangledFile.write("\n")

    # MANGLE OPTION 9
    mangle9a = option7b(name, 1)
    mangledFile.write(mangle9a)
    mangledFile.write("\n")

    mangle9b = option7b(name, 2)
    mangledFile.write(mangle9b)
    mangledFile.write("\n")

    mangle9c = option7b(name, 3)
    mangledFile.write(mangle9c)
    mangledFile.write("\n")

    mangle9d = option7b(name, 4)
    mangledFile.write(mangle9d)
    mangledFile.write("\n")