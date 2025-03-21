import tkinter as tk

from tkinter import filedialog, scrolledtext, messagebox

import os
import pickle

from Huffman import Compress, Decompress, GetFileSize

#Global Variables
compressFiles = []
decompressFilePath = None

#root setup
root = tk.Tk()
root.title("Huffman Coding Compression Tool")
root.geometry('650x700')

#Button Functions 
def AddFile():
    #Add a text file to the list of files to be compressed
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        compressFiles.append(filepath)
        filesListbox.insert(tk.END, filepath)

def RemoveFile():
    #Remove a text file from the list of files to be compressed
    selection = filesListbox.curselection()
    if selection:
        index = selection[0]
        filesListbox.delete(index)
        del compressFiles[index]


def CompressFiles():
    #Compresses the selected files
    if not compressFiles:
        messagebox.showerror("No Files Selected", "Please select some text files to compress.")
        return
    
    outputFilename = outputEntry.get().strip() or "compressed.bin"

    try:
        Compress(compressFiles, outputFilename)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def SelectDecompressFile():
    #Lets the user select a file to be decompressed
    global decompressFilePath
    filePath = filedialog.askopenfilename(filetypes=[("Compressed Files", "*.bin")])
    if filePath:
        decompressFilePath = filePath
        decompressLabel.config(text=os.path.basename(filePath))

def DecompressFile():
    if not decompressFilePath:
        messagebox.showerror("No Files Selected", "Please select a .bin file to decompress.")
        return
    
    try:
        Decompress(decompressFilePath)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    


# def details(file, output_file):
#     input_size = GetFileSize(file)
#     output_size = GetFileSize(output_file)
#     ratio = round(((output_size/input_size) * 100), 2)
#     detail = Label(root, text = f"Original: {input_size} bytes | Compressed: {output_size} | Ratio: {ratio}%", font=("Consolas", 8))
#     detail.grid(row = 2)


#-----Compression Frame-----
compressionFrame = tk.Frame(root, bd=2, relief=tk.RIDGE, padx=10, pady=10)
compressionFrame.pack(fill=tk.X, padx=10, pady=5)
compressionTitle = tk.Label(compressionFrame, text="Compression", font=("Consolas", 12, "bold"))
compressionTitle.pack()

#Listbox for files to be compressed
filesListbox = tk.Listbox(compressionFrame, width=80)
filesListbox.pack(pady=5)

#Butons to add or remove files
buttonFrame = tk.Frame(compressionFrame)
buttonFrame.pack(fill=tk.X)
AddButton = tk.Button(buttonFrame, text="Add File", command=AddFile)
AddButton.pack(side=tk.LEFT, padx=5)
RemoveButton = tk.Button(buttonFrame, text="Remove File", command=RemoveFile)
RemoveButton.pack(side=tk.LEFT, padx=5)

#Textbox to name the output compressed file
outputLabel = tk.Label(compressionFrame, text="Output Compressed File Name:")
outputLabel.pack(pady=5)
outputEntry = tk.Entry(compressionFrame, width=50)
outputEntry.pack(pady=5)
outputEntry.insert(0, "compressed.bin")

#Button to compress files
compressButton = tk.Button(compressionFrame, text="Compress Files", command=CompressFiles)
compressButton.pack(pady=5)

#-----Decompression Frame-----
decompressFrame = tk.Frame(root, bd=2, relief=tk.RIDGE, padx=10, pady=10)
decompressFrame.pack(fill=tk.X, padx=10, pady=5)
decompressTitle = tk.Label(decompressFrame, text="Decompression", font=("Consolas", 12, "bold"))
decompressTitle.pack()

#Button to select a compressed file
selectDecompressButton = tk.Button(decompressFrame, text="Select Compressed File", command=SelectDecompressFile)
selectDecompressButton.pack(pady=5)

#Label to show the selected compressed file
decompressLabel = tk.Label(decompressFrame, text="No file selected", font=("Consolas", 10))
decompressLabel.pack(pady=5)

#Button to decompress the selected file
decompressButton = tk.Button(decompressFrame, text="Decompress File", command=DecompressFile)
decompressButton.pack(pady=5)

# Exit button to close the application
exitButton = tk.Button(root, text="Exit", width=10, command=root.destroy)
exitButton.pack(pady=10)

root.mainloop()

