import heapq
import pickle
from collections import defaultdict

frequencyTable = defaultdict(int)
codeTable = defaultdict(str)
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

    if(root == None):
        return

    if(root.key != ""):
        codeTable[root.key] = currentCode
        codeTable[currentCode] = root.key
    
    huffmanGetCodes(root.left,currentCode+"0")
    huffmanGetCodes(root.right,currentCode+"1")

def huffmanSaveState(filename):

    global codeTable

    fileWriter = open(filename,"wb")
    pickle.dump(codeTable,fileWriter)

def huffmanRestoreState(filename):

    global codeTable

    fileReader = open(filename,"rb")
    codeTable = pickle.load(fileReader)

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

    codeTable["padding"] = count 

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

def huffmanReadFileBinary(filename):
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
    encodedString = encodedString[0:(length-codeTable["padding"])]

    return encodedString

def huffmanCompress(filename):
    
    content = huffmanReadFileText(filename)
    huffmanPreProcess(content)

    huffmanCreateTree()
    huffmanGetCodes(nodeHeap[0],"")

    encodedstring = huffmanGetCodedString(content)
    byteEncodedArray = huffmangetGetBytesArray(encodedstring)

    huffmanWriteToFileBinary(byteEncodedArray)
    huffmanSaveState("Codes")

def huffmanGetOriginalString(encodedString):
    
    length = len(encodedString)

    currString = ""
    decodedString = ""
    for i in range(length):
        currString += encodedString[i]
        if(codeTable[currString] != ''):
            decodedString += codeTable[currString]
            currString = ""
    
    return decodedString


def huffmanWriteToFileText(decodedString):

    fileWriter = open("huffmanDecompressed.txt","wb")
    arr = []
    for i in decodedString:
        arr.append(ord(i))
    btarr = bytearray(arr)
    fileWriter.write(btarr)

def huffmanDecompress(filename):
    
    huffmanRestoreState("Codes")
    encodedString = huffmanReadFileBinary("huffmanCompressed")

    decodedString = huffmanGetOriginalString(encodedString)
    huffmanWriteToFileText(decodedString)


# huffmanCompress("../info.txt")
huffmanDecompress("")
