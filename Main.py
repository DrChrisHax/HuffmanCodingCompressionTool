import os
import shutil
from Huffman import Compress, Decompress, GetFileSize

def TestSingleFile(fileName):
    print("==============================================")
    print("Testing single file compression/decompression for:", fileName)
    
    #Prepare filenames
    compressedFile = fileName.replace(".txt", "_compressed.bin")
    outputFolder = "decompressed_single"
    
    #Compress a single file (pass as a list with one element)
    Compress([fileName], compressedFile)
    
    #Decompress into the output folder
    Decompress(compressedFile, outputFolder)
    
    #The decompressed file will have the prefix "decompressed_"
    decompressedFile = os.path.join(outputFolder, "decompressed_" + os.path.basename(fileName))
    
    #Compare original and decompressed file contents
    with open(fileName, "r", encoding="utf-8") as fin:
        originalText = fin.read()
    with open(decompressedFile, "r", encoding="utf-8") as fin:
        decompressedText = fin.read()
    
    if originalText == decompressedText:
        print("SUCCESS: Decompressed text matches original for", fileName)
    else:
        print("ERROR: Decompressed text does not match original for", fileName)
    
    #Measure and print file sizes
    inputSize = GetFileSize(fileName)
    compressedSize = GetFileSize(compressedFile)
    decompressedSize = GetFileSize(decompressedFile)
    
    print(f"Input file '{fileName}' size: {inputSize} bytes")
    print(f"Compressed file '{compressedFile}' size: {compressedSize} bytes")
    print(f"Decompressed file '{decompressedFile}' size: {decompressedSize} bytes")
    print("==============================================\n")

def TestMultipleFiles(fileNames):
    print("==============================================")
    print("Testing multiple files compression/decompression for files:", ", ".join(fileNames))
    
    compressedFile = "multiple_compressed.bin"
    
    #Compress all files together into one .bin file
    Compress(fileNames, compressedFile)
    
    outputFolder = "decompressed_multiple"
    Decompress(compressedFile, outputFolder)
    
    totalInputSize = 0
    totalDecompressedSize = 0
    
    #Process each file and compare original to decompressed
    for fileName in fileNames:
        inputSize = GetFileSize(fileName)
        totalInputSize += inputSize
        
        decompressedFile = os.path.join(outputFolder, "decompressed_" + os.path.basename(fileName))
        decompressedSize = GetFileSize(decompressedFile)
        totalDecompressedSize += decompressedSize
        
        with open(fileName, "r", encoding="utf-8") as fin:
            originalText = fin.read()
        with open(decompressedFile, "r", encoding="utf-8") as fin:
            decompressedText = fin.read()
        
        if originalText == decompressedText:
            print(f"SUCCESS: '{fileName}' decompressed correctly.")
        else:
            print(f"ERROR: '{fileName}' decompressed incorrectly.")
        
        print(f"'{fileName}' size: {inputSize} bytes, decompressed size: {decompressedSize} bytes")
    
    compressedSize = GetFileSize(compressedFile)
    print("\nTotal input size: {} bytes".format(totalInputSize))
    print("Compressed file size: {} bytes".format(compressedSize))
    print("Total decompressed size: {} bytes".format(totalDecompressedSize))
    print("==============================================\n")

def CleanTestArtifacts():
    #Remove any created compressed files
    filesToRemove = [fileName for fileName in os.listdir() if fileName.endswith("_compressed.bin") or fileName == "multiple_compressed.bin"]
    for fileName in filesToRemove:
        print("Deleting", fileName)
        os.remove(fileName)
    
    #Remove decompressed directories if they exist
    dirsToRemove = ["decompressed_single", "decompressed_multiple"]
    for dirName in dirsToRemove:
        if os.path.isdir(dirName):
            print("Deleting directory", dirName)
            shutil.rmtree(dirName)

def Main():
    #List of test files
    singleTestFiles = ["input.txt", "shakespeare.txt", "example.txt"]
    
    #Test each file individually
    for fileName in singleTestFiles:
        TestSingleFile(fileName)
    
    #Test all files together
    TestMultipleFiles(singleTestFiles)
    
    #Clean up test artifacts after tests
    CleanTestArtifacts()

if __name__ == "__main__":
    Main()
