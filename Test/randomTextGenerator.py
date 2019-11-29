import random

def generateRandomSentece():

    sentence = ""
    for i in range(250):
        char = chr(random.randint(65,122))
        sentence += char

    sentence += '\n'
    return sentence

count = 1000
for i in range(10):
    
    filename = "../textInput/randomText/ip"+str(i+1) 
    fileWriter = open(filename+".txt","w")

    for j in range(count):
        sentence = generateRandomSentece()
        fileWriter.write(sentence)

    count += 1000