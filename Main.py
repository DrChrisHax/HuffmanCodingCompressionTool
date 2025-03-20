import os
import shutil
from Huffman import Encode, Decode, GetFileSize

def TestSingleFile(fileName):
    print("==============================================")
    print("Testing single file encoding/decoding for:", fileName)
    
    # Prepare filenames
    compressedFile = fileName.replace(".txt", "_compressed.bin")
    outputFolder = "decoded_single"
    
    # Encode a single file (pass as a list with one element)
    Encode([fileName], compressedFile)
    
    # Decode into the output folder
    Decode(compressedFile, outputFolder)
    
    # The decoded file will have the prefix "decoded_"
    decodedFile = os.path.join(outputFolder, "decoded_" + os.path.basename(fileName))
    
    # Compare original and decoded file contents
    with open(fileName, "r", encoding="utf-8") as fin:
        originalText = fin.read()
    with open(decodedFile, "r", encoding="utf-8") as fin:
        decodedText = fin.read()
    
    if originalText == decodedText:
        print("SUCCESS: Decoded text matches original for", fileName)
    else:
        print("ERROR: Decoded text does not match original for", fileName)
    
    # Measure and print file sizes
    inputSize = GetFileSize(fileName)
    compressedSize = GetFileSize(compressedFile)
    decodedSize = GetFileSize(decodedFile)
    
    print(f"Input file '{fileName}' size: {inputSize} bytes")
    print(f"Compressed file '{compressedFile}' size: {compressedSize} bytes")
    print(f"Decoded file '{decodedFile}' size: {decodedSize} bytes")
    print("==============================================\n")

def TestMultipleFiles(fileNames):
    print("==============================================")
    print("Testing multiple files encoding/decoding for files:", ", ".join(fileNames))
    
    compressedFile = "multiple_compressed.bin"
    
    # Encode all files together into one .bin file
    Encode(fileNames, compressedFile)
    
    outputFolder = "decoded_multiple"
    Decode(compressedFile, outputFolder)
    
    totalInputSize = 0
    totalDecodedSize = 0
    
    # Process each file and compare original to decoded
    for fileName in fileNames:
        inputSize = GetFileSize(fileName)
        totalInputSize += inputSize
        
        decodedFile = os.path.join(outputFolder, "decoded_" + os.path.basename(fileName))
        decodedSize = GetFileSize(decodedFile)
        totalDecodedSize += decodedSize
        
        with open(fileName, "r", encoding="utf-8") as fin:
            originalText = fin.read()
        with open(decodedFile, "r", encoding="utf-8") as fin:
            decodedText = fin.read()
        
        if originalText == decodedText:
            print(f"SUCCESS: '{fileName}' decoded correctly.")
        else:
            print(f"ERROR: '{fileName}' decoded incorrectly.")
        
        print(f"'{fileName}' size: {inputSize} bytes, decoded size: {decodedSize} bytes")
    
    compressedSize = GetFileSize(compressedFile)
    print("\nTotal input size: {} bytes".format(totalInputSize))
    print("Compressed file size: {} bytes".format(compressedSize))
    print("Total decoded size: {} bytes".format(totalDecodedSize))
    print("==============================================\n")

def CleanTestArtifacts():
    # Remove any created compressed files
    filesToRemove = [fileName for fileName in os.listdir() if fileName.endswith("_compressed.bin") or fileName == "multiple_compressed.bin"]
    for fileName in filesToRemove:
        print("Deleting", fileName)
        os.remove(fileName)
    
    # Remove decoded directories if they exist
    dirsToRemove = ["decoded_single", "decoded_multiple"]
    for dirName in dirsToRemove:
        if os.path.isdir(dirName):
            print("Deleting directory", dirName)
            shutil.rmtree(dirName)

def Main():
    # List of test files
    singleTestFiles = ["input.txt", "shakespeare.txt", "example.txt"]
    
    # Test each file individually
    for fileName in singleTestFiles:
        TestSingleFile(fileName)
    
    # Test all files together
    TestMultipleFiles(singleTestFiles)
    
    # Clean up test artifacts after tests
    CleanTestArtifacts()

if __name__ == "__main__":
    Main()
