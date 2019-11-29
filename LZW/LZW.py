from collections import defaultdict
import os
import pickle



metaData = {}

table = defaultdict(int)

def initializeTable():
    global table
    for i in range(256):
        table[chr(i)] = i
        table[i] = chr(i)
    
    
def encode(string):
    
    global table

    length = len(string)

    initializeTable()

    frontChar = string[0]

    outputCode = []

    count = 256

    for i in range(1,length):
        next_char = string[i]
        if(table[frontChar+next_char] != 0):
            frontChar = frontChar+next_char
        else:
            # print(frontChar,table[frontChar])
            outputCode.append(table[frontChar])
            if(count <= 4000):
                table[frontChar+next_char] = count
                count += 1
            frontChar = next_char
    outputCode.append(table[frontChar])
    # print(outputCode)
    return outputCode
    
def decode(outputCode):
    
    global table

    length = len(outputCode)

    initializeTable()

    old = outputCode[0]
    C = table[old]

    original = []
    original.append(C)

    count = 255

    for i in range(1,length):
        new = outputCode[i]
        count += 1
        if(table[new] == 0):
            S = table[old]
            S = S + C
        else:
            S = table[new]
        original.append(S)
        C = S[0]
        table[count] = table[old] + C
        old = new

    decodedString = ("").join(original)
    return decodedString

def get8BitCodes(codes):
    res = []

    n=len(codes)

    if(n%2 != 0):
        codes.append(0)

    n = n+1

    for i in range(0,n-1,2):
        upperEight = codes[i]>>4
        lowerFour = codes[i]&0x0F
        
        num1 = upperEight
        num2 = lowerFour<<4

        secondNumUp = codes[i+1]>>8
        num2 = num2|secondNumUp

        num3 = codes[i+1]&0xFF

        res.append(num1)
        res.append(num2)
        res.append(num3)
    return res

def getOriginalCodes(eightBitVal):
    length = len(eightBitVal)

    original = []

    for i in range(0,length-2,3):
        num1 = eightBitVal[i]
        num2 = eightBitVal[i+1]
        num3 = eightBitVal[i+2]

        or1 = (num1<<4)|(num2>>4)
        or2 = ((num2&0x0F)<<8)|num3

        # print(num1,num2,num3,or1,or2)    

        original.append(or1)
        original.append(or2)
    if(original[len(original)-1] == 0):
        original.pop()
    return original

def readFileBinary(filename):
    fileWriter = open(filename,"rb")
    curr = fileWriter.read(1) 
    eightBitVal = []
    while(curr != b""):
        temp = int.from_bytes(curr,byteorder='big')
        eightBitVal.append(temp)
        curr = fileWriter.read(1)
    
    return eightBitVal
def readFileText(fullname):

    fileReader =open(fullname,'rb') 

    curr = fileReader.read(1) 
    content = ""
    while(curr != b""):
        content += chr(ord(curr))
        curr = fileReader.read(1)

    return content

def writeTofileBinary(eightBitVal):

    fileWriter = open("compressed","wb")
    fileByteArray = bytearray(eightBitVal)
    fileWriter.write(fileByteArray)


def writeToFileText(string):

    fileWriter = open("decompressed","w")
    fileWriter.write(string)

def writeToFileDecompresedOutput(decodedString):

    fileWriter = open("LZWDecompressed"+metaData['f'],"wb")
    arr = []
    for i in decodedString:
        arr.append(ord(i))
    btarr = bytearray(arr)
    fileWriter.write(btarr)

def saveState(filename):

    global metaData
    
    with open(filename,"wb") as dictHandle:
        pickle.dump(metaData,dictHandle)

def restoreSate(filename):

    global metaData

    with open(filename,"rb") as dictHandle:
        metaData = pickle.load(dictHandle)

def compress(fullname):

    global metaData
    
    filename, file_extension = os.path.splitext(fullname)
    metaData["f"] = file_extension

    string = readFileText(fullname)
    encodedVal = encode(string)

    eightBitVal = get8BitCodes(encodedVal)

    saveState("fileFormat")
    
    writeTofileBinary(eightBitVal)


def decompress(filename):

    restoreSate("fileFormat")
    
    eightBitVal = readFileBinary(filename)
    originalCodes = getOriginalCodes(eightBitVal)

    decodedString = decode(originalCodes)
    
    writeToFileDecompresedOutput(decodedString)



# compress("ip10.txt")
# decompress("compressed")
