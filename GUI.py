import tkinter as tk

import os
import pickle 

from tkinter import filedialog, messagebox, scrolledtext
from Huffman import Compress, Decompress, GetFileSize
from DrawHuffmanTree import ShowHuffmanTree

#Global Variables
compressFiles = []
totalSize = 0 #Running total of size of all files uploaded
decompressFilePath = None

#Button Functions 
def AddFile():
    #Add a text file to the list of files to be compressed
    global totalSize
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        fileSize = GetFileSize(filepath)  #Get file size in bytes
        compressFiles.append(filepath)
        #Insert file path along with its size into the listbox
        filesListbox.insert(tk.END, f"{filepath} - {fileSize} bytes")
        totalSize += fileSize
        totalSizeLabel.config(text=f"Total Size: {totalSize} bytes")

def RemoveFile():
    #Remove a text file from the list of files to be compressed
    global totalSize
    selection = filesListbox.curselection()
    if selection:
        index = selection[0]
        removedFile = compressFiles.pop(index)
        fileSize = GetFileSize(removedFile)
        totalSize -= fileSize
        filesListbox.delete(index)
        totalSizeLabel.config(text=f"Total Size: {totalSize} bytes")


def CompressFiles():
    #Compresses the selected files
    if not compressFiles:
        messagebox.showerror("No Files Selected", "Please select some text files to compress")
        return
    
    outputFilename = outputEntry.get().strip() or "compressed.bin"

    try:
        Compress(compressFiles, outputFilename)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
    #update the huffman codes textbox
    try:
        with open(outputFilename, "rb") as infile:
            data = pickle.load(infile)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load compressed file: {e}")
        return
    codeTable = data.get("t")

    codes = ""
    for char, code in codeTable.items():
        codes += (char + " : " + code + "\n")
    codebox.configure(state='normal')
    codebox.delete("1.0", tk.END)
    codebox.insert(tk.INSERT, codes)
    codebox.configure(state='disabled')
    
    #get compressed filesize and size ratio
    compressed_filesize = GetFileSize(outputFilename)
    ratio = round(((compressed_filesize/totalSize) * 100), 2)
    compdetails.config(text=f"Compressed Size : {compressed_filesize} Bytes | Ratio : {ratio}%")

def SelectDecompressFile():
    #Lets the user select a file to be decompressed
    global decompressFilePath
    filePath = filedialog.askopenfilename(filetypes=[("Compressed Files", "*.bin")])
    if filePath:
        decompressFilePath = filePath
        decompressLabel.config(text=os.path.basename(filePath))
        fileSize = GetFileSize(filePath)
        compressedSizeLabel.config(text=f"Compressed File Size: {fileSize} bytes")

def DecompressFile():
    if not decompressFilePath:
        messagebox.showerror("No Files Selected", "Please select a .bin file to decompress")
        return
    
    try:
        contents = Decompress(decompressFilePath)
    except Exception as e:
        messagebox.showerror("Error", str(e))

    #update the textbox for the decompressed contents
    decompressedbox.configure(state="normal")
    decompressedbox.delete("1.0", tk.END)
    decompressedbox.insert(tk.INSERT, contents)
    decompressedbox.configure(state="disabled")
    
#Tree drawing function
def ShowHuffmanTreeDialog():
    #Do the validations first
    #Then call the helper function in the other file
    if decompressFilePath is None:
        messagebox.showerror("No Files Selected", "Please select a .bin file to view the tree of")
        return
    
    try:
        with open(decompressFilePath, "rb") as infile:
            data = pickle.load(infile)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load compressed file: {e}")
        return 
    
    codeTable = data.get("t")
        
    if codeTable is None:
        messagebox.showerror("Error", "No Huffman code table found in the file")
        return 
    
    ShowHuffmanTree(codeTable, root)

#-----UI-----

#root setup
root = tk.Tk()
root.title("Huffman Coding Compression Tool")
root.geometry('1920x1080')
root.attributes('-zoomed', True)

#Main frame to hold other frames
mainFrame = tk.Frame(root)
mainFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

#-----Compression Frame-----
compressionFrame = tk.Frame(mainFrame, bd=2, relief=tk.RIDGE, padx=10, pady=10)
compressionFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
compressionTitle = tk.Label(compressionFrame, text="Compression", font=("Consolas", 12, "bold"))
compressionTitle.pack()

#Listbox for files to be compressed
filesListbox = tk.Listbox(compressionFrame, width=80, height=4)
filesListbox.pack(fill=tk.X, pady=5)

#Total sizes of input files
totalSizeLabel = tk.Label(compressionFrame, text="Total Size: 0 bytes", font=("Consolas", 10))
totalSizeLabel.pack(pady=5)

#compressed filesize and ratio Label
compdetails = tk.Label(compressionFrame, text = "Compressed Size : -- Bytes | Ratio : --%", font=("Consolas", 8))
compdetails.pack(pady=5)

#Butons to add or remove files
buttonFrame = tk.Frame(compressionFrame)
buttonFrame.pack(fill=tk.X, pady=5)
AddButton = tk.Button(buttonFrame, text="Add File", font=("Consolas", 10), command=AddFile)
RemoveButton = tk.Button(buttonFrame, text="Remove File", font=("Consolas", 10), command=RemoveFile)
AddButton.pack(side=tk.LEFT, expand=True, padx=5)
RemoveButton.pack(side=tk.LEFT, expand=True, padx=5)

#Textbox to name the output compressed file
outputLabel = tk.Label(compressionFrame, text="Output Compressed File Name:", font=("Consolas", 10))
outputLabel.pack(pady=5)
outputEntry = tk.Entry(compressionFrame, width=50)
outputEntry.pack(fill=tk.X, pady=5)
outputEntry.insert(0, "compressed.bin")

#Button to compress files
compressButton = tk.Button(compressionFrame, text="Compress Files", font=("Consolas", 10), command=CompressFiles)
compressButton.pack(pady=5)

#Textbox for codes and label for it
codelabel = tk.Label(compressionFrame, text="Huffman Codes", font=("Consolas", 10))
codelabel.pack(pady=5)
codebox = scrolledtext.ScrolledText(compressionFrame, wrap=tk.WORD, width=50, height=6, font=("Consolas", 8))
codebox.configure(state='disabled')
codebox.pack(fill=tk.X, pady=5)


#-----Decompression Frame-----
decompressFrame = tk.Frame(mainFrame, bd=2, relief=tk.RIDGE, padx=10, pady=10)
decompressFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
decompressTitle = tk.Label(decompressFrame, text="Decompression", font=("Consolas", 12, "bold"))
decompressTitle.pack()

#Button to select a compressed file
selectDecompressButton = tk.Button(decompressFrame, text="Select Compressed File", font=("Consolas", 10), command=SelectDecompressFile)
selectDecompressButton.pack(pady=5)

#Label to show the selected compressed file
decompressLabel = tk.Label(decompressFrame, text="No file selected", font=("Consolas", 8))
decompressLabel.pack(pady=5)

#Label to show the size of the compressed file
compressedSizeLabel = tk.Label(decompressFrame, text="Compressed File Size: 0 bytes", font=("Consolas", 8))
compressedSizeLabel.pack(pady=5)

#Button to decompress the selected file
decompressButton = tk.Button(decompressFrame, text="Decompress File", font=("Consolas", 10), command=DecompressFile)
decompressButton.pack(pady=5)

#Button to show the huffman tree of the selected file
huffmanTreeButton = tk.Button(decompressFrame, text="Show Huffman Tree", font=("Consolas", 10), command=ShowHuffmanTreeDialog)
huffmanTreeButton.pack(pady=5)

#Textbox for decompressed text and label for it
decomlabel = tk.Label(decompressFrame, text="Decompressed Text", font=("Consolas", 10))
decomlabel.pack(pady=5)
decompressedbox = scrolledtext.ScrolledText(decompressFrame, wrap=tk.WORD, width=50, height=6, font=("Consolas", 8))
decompressedbox.configure(state='disabled')
decompressedbox.pack(fill=tk.X, pady=5)

#Exit button to close the application
exitButton = tk.Button(root, text="Exit", font=("Consolas", 10), width=10, command=root.destroy)
exitButton.pack(pady=10)

root.mainloop()

