from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext

from Huffman import Compress, Decompress, GetFileSize
import os

#root setup
root = Tk()
root.grid_columnconfigure(0, weight=1)
root.title("Huffman Coding Compression Tool")
root.geometry('450x400')

def compress_button():
    #opens file, runs encoder, updates the compression details label
    #NEEDS TO: get the huffman codes in a way that can be interacted with
    #          update row 3 text box
    file = openFile()
    compressed_file = file.replace(".txt", ".bin")
    Compress(file, compressed_file)

    
    detail.grid_forget()
    details(file, compressed_file)

def decompress_button():
    #NEEDS TO: run decoder, check to see if decoded properly.
    pass

def openFile():
    filepath = filedialog.askopenfilename()
    return filepath

def details(file, output_file):
    input_size = GetFileSize(file)
    output_size = GetFileSize(output_file)
    ratio = round(((output_size/input_size) * 100), 2)
    detail = Label(root, text = f"Original: {input_size} bytes | Compressed: {output_size} | Ratio: {ratio}%", font=("Consolas", 8))
    detail.grid(row = 2)

#row 0, title label
title = Label(root, text="Huffman Coding Compression Tool\n", font=("Consolas", 12))
title.grid(row=0)
#title.grid_columnconfigure(1, weight=1)

#row 1, select text file button
select = Button(text ="Select Text File", font=("Consolas", 8), command=compress_button)
select.grid(row=1)

#row 2, compression details label (tied to "compress_button" function)
detail = Label(root, text="Compression details will appear here", font=("Consolas", 8))
detail.grid(row = 2)

#row 3, "huffman codes" label
l2 = Label(root, text="Huffman Codes", font=("Consolas", 10))
l2.grid(row=3)

#row 4, scrolled text box 1
box1 = scrolledtext.ScrolledText(root, wrap = WORD, width = 50, height = 7, font = ("Consolas", 8))
box1.configure(state = 'disabled')
box1.grid(row = 4)

#row 5, "decompress file" button
decom = Button(text ="Decompress File", font=("Consolas", 8), command=decompress_button)
decom.grid(row=5)

#row 6, "decoded text" label
l2 = Label(root, text="Decoded Text", font=("Consolas", 10))
l2.grid(row=6)

#row 7, scrolled text box 2
box2 = scrolledtext.ScrolledText(root, wrap = WORD, width = 50, height = 5, font = ("Consolas", 8))
box2.configure(state = 'disabled')
box2.grid(row = 7)

#row 8, "exit" button
exit_ = Button(root, text='Exit', width=10, command=root.destroy)
exit_.grid(row=8)

root.mainloop()

