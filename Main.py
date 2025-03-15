from Huffman import Encode, Decode

def main():
    # Run encoding: input.txt -> compressed.bin
    print("Encoding input.txt to compressed.bin...")
    Encode("input.txt", "compressed.bin")
    
    # Run decoding: compressed.bin -> output.txt
    print("Decoding compressed.bin to output.txt...")
    Decode("compressed.bin", "output.txt")
    
    # Verify that the decoded output matches the original input
    with open("input.txt", "r", encoding="utf-8") as fin:
        original = fin.read()
    with open("output.txt", "r", encoding="utf-8") as fout:
        decoded = fout.read()
    
    if original == decoded:
        print("Success: The decoded text matches the original input!")
    else:
        print("Error: The decoded text does not match the original input.")

if __name__ == "__main__":
    main()