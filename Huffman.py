import heapq
import pickle
from bitarray import bitarray

class HuffmanNode:
    #This class is the structure for a Node in the Huffman Tree
    #Each node has 
        #A frequency for the character
        #A character (only if it isn't an internal Node)
        #A Left Child
        #A Right Child
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    
    #Comparison Overrides
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __gt__(self, other):
        return self.freq > other.freq
    
    
def CountFrequency(text):
    #This takes an input string and counts the occurance
    #of each character
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq

def BuildHuffmanTree(frequency):
    #This builds the Huffman tree based on char frequency
    #and returns the root node of the tree
    heap = []
    for char, freq in frequency.items():
        node = HuffmanNode(freq, char)
        heapq.heappush(heap, node)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left.freq + right.freq, None, left, right)
        heapq.heappush(heap, merged)
    
    return heap[0] if heap else None

def GenerateHuffmanCodes(node, prefix=""):
    #Recursively traverse the tree to generate binary codes
    #This function takes in the current node and the prefix built so far
    #then returns a dictionary mapping characters to their codes

    if node is None:
        return {}
    
    if node.char is not None:
        #This is a leaf node
        return {node.char: prefix or "0"} #If prefix is none (ie single char) then it will just have a code of "0"
    
    codes = {}
    codes.update(GenerateHuffmanCodes(node.left, prefix + "0"))
    codes.update(GenerateHuffmanCodes(node.right, prefix + "1"))
    return codes

def Encode(inputFilepath = "input.txt", outputFilepath = "compressed.bin"):
    #This will encode the contents of inputFilepath
    #The output file will contain a pickled dictionary with two keys
        #codeTable -> the Huffman codes mapping char to binary string
        #encodedData -> the compressed bitarray of the input text
    
    with open(inputFilepath, "r", encoding="utf-8") as infile:
        text = infile.read()
    
    if not text:
        print("Input file is empty")
        return
    
    frequency = CountFrequency(text)
    tree = BuildHuffmanTree(frequency)
    codeTable = GenerateHuffmanCodes(tree)

    encodedString = "".join(codeTable[ch] for ch in text)
    encodedBits = bitarray(encodedString)

    with open(outputFilepath, "wb") as outfile:
        pickle.dump({"0": codeTable, "1": encodedBits}, outfile)

def Decode(inputFilepath="compressed.bin", outputFilepath="output.txt"):
    #This takes a .bin file produced by the Encode function and converts it back into text
    #The file should contain a pickled dictionary with:
        #0 -> the huffman codes with char to binary
        #1 -> the bitarray of encoded data
    #The decoded text is written to outputFilepath

    with open(inputFilepath, "rb") as infile:
        data = pickle.load(infile)

    codeTable = data["0"]
    encodedBits = data["1"]

    bitString = encodedBits.to01()
    reverseCodeTable = {code: char for char, code in codeTable.items()}
    decodedText = ""
    currentCode = ""
    for bit in bitString:
        currentCode += bit
        if currentCode in reverseCodeTable:
            decodedText += reverseCodeTable[currentCode]
            currentCode = ""

    with open(outputFilepath, "w", encoding="utf-8") as outfile:
        outfile.write(decodedText)
    
