import os
from Huffman import Encode, Decode, GetFileSize

def TestHuffman(file_name):
    compressed_file = file_name.replace(".txt", ".bin")
    output_file = file_name.replace(".txt", "_output.txt")
    
    # Run encoding
    print(f"Encoding {file_name} to {compressed_file}...")
    Encode(file_name, compressed_file)
    
    # Run decoding
    print(f"Decoding {compressed_file} to {output_file}...")
    Decode(compressed_file, output_file)
    
    # Verify that the decoded output matches the original input
    with open(file_name, "r", encoding="utf-8") as fin:
        original = fin.read()
    with open(output_file, "r", encoding="utf-8") as fout:
        decoded = fout.read()
    
    if original == decoded:
        print(f"Success: The decoded text matches the original input for {file_name}!")
    else:
        print(f"Error: The decoded text does not match the original input for {file_name}.")
    
    input_size = GetFileSize(file_name)
    compressed_size = GetFileSize(compressed_file)
    output_size = GetFileSize(output_file)
    
    print(f"{file_name} size in bytes: {input_size}")
    print(f"{compressed_file} size in bytes: {compressed_size}")
    print(f"{output_file} size in bytes: {output_size}")

def Clean():
    for file in os.listdir():
        if file.endswith(".bin") or file.endswith("_output.txt"):
            print(f"Deleting {file}...")
            os.remove(file)

def main():
    TestHuffman("input.txt")
    TestHuffman("shakespeare.txt")
    Clean()

if __name__ == "__main__":
    main()
