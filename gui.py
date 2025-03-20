import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

from Huffman import Compress, Decompress, GetFileSize

#This UI will have two text fields

#The first text field will be a list of files to compress
#You can add a file by clicking the add button
#You can remove a file by clicking the remove button
#You can compress those files by clicking the compress button
#There also will be a text box where you can name the compressed file

#The second text field will be a single file to decompress
#You can load in a compressed .bin file
#There will be a button to decompress the file
#There will be a button to view the Huffman Tree in the file (implement later)

#Global Varaiables ---------------------------------------------------------------------
compressFiles = []
decompressFilePath = None

#Button Functions -----------------------------------------------------------------------
def AddFile():
    #Open a file dialog and select a text file to add to the compression list
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        compressFiles.append(filepath)
        filesListTextbox.insert(tk.END, filepath)

def RemoveFile():
    #Remove the last file added to the list
    selection = filesListTextbox.curselection()
    if selection:
        index = selection[0]
        filesListTextbox.delete(index)
        del compressFiles[index]

def CompressButton():
    #Compresses the selected files
    if not compressFiles:
        messagebox.showerror("No Files Selected", "Please select some text files to compress.")
        return 
    
    #Function not complete

def SelectDecompressFile():
    pass

def DecompressButton():
    pass

def ShowHuffmanTree():
    #This function will open another dialog that shows the 
    #Huffman Tree stored in the current compressed file
    pass



    
    

#UI Setup ----------------------------------------------------------------

root = tk.Tk()
root.grid_columnconfigure(0, weight=1)
root.title("Huffman Coding Compression Tool")
root.geometry('650x700')


#Files Listbox
filesListTextbox = tk.Listbox(width= 80, height=5)



root.mainloop()
