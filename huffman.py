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

    if(remain != 0):
        while(remain != 8):
            encodedString += "0"
            remain += 1

    codeTable["padding"] = remain

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

def huffmanCompress(filename):
    
    content = huffmanReadFileText(filename)
    huffmanPreProcess(content)

    huffmanCreateTree()
    huffmanGetCodes(nodeHeap[0],"")

    encodedstring = huffmanGetCodedString(content)
    byteEncodedArray = huffmangetGetBytesArray(encodedstring)

    huffmanWriteToFileBinary(byteEncodedArray)
    huffmanSaveState("Codes")
    


node1 = Node("A",0.35,None,None)
node2 = Node("B",0.1,None,None)
node3 = Node("C",0.2,None,None)
node4 = Node("D",0.2,None,None)
node5 = Node("f",0.15,None,None)

# nodeHeap = [node1,node2,node3,node4,node5]
# heapq.heapify(nodeHeap)

# huffmanCreateTree()

# huffmanGetCodes(nodeHeap[0],"")

# for i in codeTable:
#     print(i,codeTable[i])

# print(node1,node2,node3) 
# arr = [node1,node2,node3]
# 
# heapq.heapify(arr)
# 
# print(arr)

huffmanCompress("info.txt")
