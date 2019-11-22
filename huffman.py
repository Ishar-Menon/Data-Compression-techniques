import heapq
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
# node1 = Node(3,1)
# node2 = Node(1,2)
# node3 = Node(2,3)
# 
# print(node1,node2,node3)
# 
# 
# 
# arr = [node1,node2,node3]
# 
# heapq.heapify(arr)
# 
# print(arr)


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
        nodeHeap.append(Node(i,frequencyTable[i],None.None))

    heapq.heapify(nodeHeap)

def huffmanCreateTree():

    global nodeHeap

    size = len(nodeHeap)

    while(size > 1):

        firstNode = heapq.heappop(nodeHeap)
        secondNode = heapq.heappop(nodeHeap)

        combination = Node("",firstNode.frequency+secondNode.frequency,firstNode,secondNode)

        heapq.heappush(combination)

        size -= 1

def huffmanGetCodes():
    pass