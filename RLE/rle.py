def rleEncode(string):
    
    length = len(string)
    index = 1

    encodedString = ""

    currChar = string[0]
    count = 1

    while(index < length):

        if(string[index] != currChar):
            if(count != 1):
                encodedString += (currChar + str(count))
            else:
                encodedString += currChar
            currChar = string[index]
            count = 1   
        else:
            count += 1

        if(index == (length-1)):
            if(count != 1):
                encodedString += (currChar + str(count))
            else:
                encodedString += currChar
        index += 1


    return encodedString

def isNum(n):
    if(ord(n) >= 48 and  ord(n) <= 57):
        return 1
    return 0

def rleDecode(encodedString):
    
    decodedString = ""

    length = len(encodedString)

    currChar = encodedString[0]
    currNum = 0
    index = 1

    while(index < length):
        
        if(isNum(encodedString[index])):
            currNum = currNum*10 + int(encodedString[index])
        else:
            
            if(currNum == 0):
                decodedString += currChar
            else:
                for i in range(currNum):
                    decodedString += currChar

            currChar = encodedString[index]
            currNum = 0
    
        index += 1
    
    if(currNum == 0):
        decodedString += currChar
    else:
        for i in range(currNum):
            decodedString += currChar

    return decodedString

def rleReadFile(fullname):

    fileReader =open(fullname,'rb') 

    curr = fileReader.read(1) 
    content = ""
    while(curr != b""):
        content += chr(ord(curr))
        curr = fileReader.read(1)

    return content

def rleWriteFile(content,filename):

    fileWriter = open(filename,"w")
    fileWriter.write(content)


def rleCompress(filename):
    
    content = rleReadFile(filename)
    encodedString = rleEncode(content)
    rleWriteFile(encodedString,"compressed.txt")

def rleDecompress(filename):
    content = rleReadFile("compressed.txt")
    decodedString = rleDecode(content)
    rleWriteFile(decodedString,"decoded.txt")

ip = "wwwwraaadexxxxxxywwwmh"

rleCompress("../info.txt")
rleDecompress("")