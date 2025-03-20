import heapq
import pickle
import os
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

def Encode(inputFilepaths, outputFilepath = "compressed.bin"):
    #This will encode the contents of all the inputed files
    #The output file will contain a pickled dictionary with two keys
        #codeTable -> the Huffman codes mapping char to binary string
        #encodedData -> the compressed bitarray of the input texts

    allText = ""
    for filepath in inputFilepaths:
        with open(filepath, "r", encoding="utf-8") as infile:
            allText += infile.read()
    
    if not allText:
        print("No data found int he selected files.")
        return

    #This will build the tree based on the frequency of all the texts
    frequency = CountFrequency(allText)
    tree = BuildHuffmanTree(frequency)
    codeTable = GenerateHuffmanCodes(tree)

    encodedFiles = []
    for filepath in inputFilepaths:
        with open(filepath, "r", encoding="utf-8") as infile:
            text = infile.read()
        encodedString = "".join(codeTable[ch] for ch in text)
        encodedBits = bitarray(encodedString)
        file_entry = {
            "f": os.path.basename(filepath), #f for filename
            "d": encodedBits                 #d for data
        }
        encodedFiles.append(file_entry)

    outputData = {
        "t": codeTable,         #t for tree
        "e": encodedFiles       #e for encoded files
    }
    with open(outputFilepath, "wb") as outfile:
        pickle.dump(outputData, outfile)

def Decode(inputFilepath="compressed.bin", outputDir="decoded_files"):
    #This takes a .bin file produced by the Encode function and converts it back into multiple text files
    #The file should contain a pickled dictionary with:
        #"t": the global Huffman code table (from the global tree)
        #"e": a list of file entries, where each entry is a dictionary with:
            #"f": the original filename
            #"d": the encoded bitarray data
    #The decoded text is written to outputFilepath

    with open(inputFilepath, "rb") as infile:
        data = pickle.load(infile)

    codeTable = data["t"]
    encodedFiles = data["e"]

    reverseCodeTable = {code: char for char, code in codeTable.items()}

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    for file_entry in encodedFiles:
        filename = file_entry["f"]
        encodedBits = file_entry["d"]

        bitString = encodedBits.to01()
        decodedText = ""
        currentCode = ""
        for bit in bitString:
            currentCode += bit
            if currentCode in reverseCodeTable:
                decodedText += reverseCodeTable[currentCode]
                currentCode = ""

        outputPath = os.path.join(outputDir, f"decoded_{filename}")
        with open(outputPath, "w", encoding="utf-8") as outfile:
            outfile.write(decodedText)    

def GetFileSize(filepath):
    #This takes a file path and returns the
    #size in bytes of the file but we can
    #change the return type later based on what
    #our UI needs

    try:
        sizeBytes = os.path.getsize(filepath)
        #sizeKB = sizeBytes / 1024
        #sizeMB = sizeKB / 1024
        #sizeGB = sizeMB / 1024

        return sizeBytes
    except FileNotFoundError:
        return "File not found"
    
