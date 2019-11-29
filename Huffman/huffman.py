import heapq
import pickle
import os
from collections import defaultdict

frequencyTable = defaultdict(int)
codeTable = defaultdict(str)
revCodeTable = defaultdict(str)
nodeHeap = []

class Node:
    def __init__(self,key,frequency,left,right):
        self.key = key
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, value):
        if(self.frequency <= value.frequency):
            return True
        else:
            return False


def huffmanReadFileText(filename):
    
    fileReader = open(filename,"r")
    content = fileReader.read()
    
    return content

def huffmanReadFileImage(filename):

    fileReader = open(filename,"rb")
    curr = fileReader.read(1) 
    content = ""
    while(curr != b""):
        charNo = int.from_bytes(curr,byteorder='big')
        content += chr(charNo)
        curr = fileReader.read(1)

    return content

def huffmanPreProcess(content):

    global frequencyTable
    global nodeHeap
 
    for i in content:
        frequencyTable[i] += 1

    for i in frequencyTable:
        nodeHeap.append(Node(i,frequencyTable[i],None,None))

    heapq.heapify(nodeHeap)

def huffmanCreateTree():

    global nodeHeap

    size = len(nodeHeap)

    while(size > 1):

        firstNode = heapq.heappop(nodeHeap)
        secondNode = heapq.heappop(nodeHeap)

        combination = Node("",firstNode.frequency+secondNode.frequency,firstNode,secondNode)

        heapq.heappush(nodeHeap,combination)

        size -= 1

def huffmanGetCodes(root,currentCode):
    
    global codeTable
    global revCodeTable

    if(root == None):
        return

    if(root.key != ""):
        codeTable[root.key] = currentCode
        revCodeTable[currentCode] = root.key
    
    huffmanGetCodes(root.left,currentCode+"0")
    huffmanGetCodes(root.right,currentCode+"1")

def huffmanSaveState(filename):

    global revCodeTable

    fileWriter = open(filename,"wb")
    pickle.dump(revCodeTable,fileWriter)

def huffmanRestoreState(filename):

    global revCodeTable

    fileReader = open(filename,"rb")
    revCodeTable = pickle.load(fileReader)

def huffmanGetCodedString(content):

    global codeTable

    encodedString = ""
    for i in content:
        encodedString += codeTable[i]

    remain = len(encodedString)%8

    count = 0
    if(remain != 0):
        while(remain != 8):
            encodedString += "0"
            remain += 1
            count += 1

    revCodeTable["padding"] = count 

    return encodedString


def huffmangetGetBytesArray(encodedString):
    
    encodedArray = []
    
    for i in range(0,len(encodedString),8):
        binNum = encodedString[i:i+8]
        num = int(binNum,2)
        encodedArray.append(num)

    byteEncodedArray = bytearray(encodedArray)
    
    return byteEncodedArray


def huffmanWriteToFileBinary(byteEncodedArray):
    
    fileWriter = open("huffmanCompressed","wb")
    fileWriter.write(byteEncodedArray)

def huffmanReadFileCompressedBinary(filename):
    fileReader = open(filename,"rb")
    curr = fileReader.read(1) 
    eightBitVal = []
    encodedString = ""
    while(curr != b""):
        asciiVal = int.from_bytes(curr,byteorder='big')
        binVal = bin(asciiVal)[2:].rjust(8, '0')
        encodedString += binVal
        curr = fileReader.read(1)

    length = len(encodedString)
    encodedString = encodedString[0:(length-revCodeTable["padding"])]

    return encodedString

def huffmanWriteToFileText(decodedString):

    fileWriter = open("huffmanDecompressed"+revCodeTable['exten'],"wb")
    arr = []
    for i in decodedString:
        arr.append(ord(i))
    btarr = bytearray(arr)
    fileWriter.write(btarr)

def huffmanReadInputFile(fullname):
    
    fileReader =open(fullname,'rb') 

    curr = fileReader.read(1) 
    content = ""
    while(curr != b""):
        content += chr(ord(curr))
        curr = fileReader.read(1)

    return content
def huffmanCompress(fullname):

    global revCodeTable
    
    filename, file_extension = os.path.splitext(fullname) 

    content = huffmanReadInputFile(fullname)
    huffmanPreProcess(content)

    huffmanCreateTree()
    huffmanGetCodes(nodeHeap[0],"")

    encodedstring = huffmanGetCodedString(content)
    byteEncodedArray = huffmangetGetBytesArray(encodedstring)

    huffmanWriteToFileBinary(byteEncodedArray)

    revCodeTable['exten'] = file_extension
    huffmanSaveState("Codes")

def huffmanGetOriginalString(encodedString):
    
    length = len(encodedString)

    currString = ""
    decodedString = ""
    for i in range(length):
        currString += encodedString[i]
        if(revCodeTable[currString] != ''):
            decodedString += revCodeTable[currString]
            # print(codeTable[currString],currString)
            currString = ""
    
    return decodedString


def huffmanDecompress(filename):
    
    huffmanRestoreState("Codes")
    encodedString = huffmanReadFileCompressedBinary("huffmanCompressed")

    decodedString = huffmanGetOriginalString(encodedString)
    huffmanWriteToFileText(decodedString)


# huffmanCompress("../Test/ip1.txt")
# huffmanDecompress("")
# huffmanRestoreState("Codes")
# encodedString = huffmanReadFileBinary("huffmanCompressed")
# dcs = huffmanGetOriginalString(encodedString)
# print(codeTable["1"])
# print(dcs)
# text = huffmanReadFileImage("img.jpg")
# print(text)

# make seperate tables

