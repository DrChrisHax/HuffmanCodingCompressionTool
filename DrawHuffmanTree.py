import tkinter as tk

def BuildTreeFromCodeTable(codeTable):
    #This function takes in a code table
    #and rebuilds the huffman tree from it
    tree = {}
    for char, code in codeTable.items():
        current = tree
        for bit in code:
            if bit not in current:
                current[bit] = {}
            current = current[bit]
        current['char'] = char #Store the character at each leaf
    return tree

def DrawTree(canvas, tree, x, y, xOffset, levelHeight = 50):
    #This function will recursively draw the tree on a canvas
    radius = 20 #Node size

    #First, if the node is a leaf, draw the char. Otherwise, leave it blank
    label = tree.get('char', '')
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="white")
    canvas.create_text(x, y, text=label)

    #For each branch (0 for left, 1 for right), draw the connecting line
    #and recursively draw the subtree
    for bit in ['0', '1']:
        if bit in tree:
            child = tree[bit]
            childX = x - xOffset if bit == '0' else x + xOffset
            childY = levelHeight
            canvas.create_line(x, y + radius, childX, childY - radius)

            #Add the label to the line
            midX = (x + childX) / 2
            midY = (y + childY) / 2
            canvas.create_text(midX, midY, text=bit)
            DrawTree(canvas, child, childX, childY, xOffset * 0.7, levelHeight + 50)

def ShowHuffmanTree(codeTable, rootUIElement):
    #DO ALL VALIDATION BEFORE CALLING THIS FUNCTION
    #This function will take in a code table (straight from the .bin file)
    #and the root UI element

    tree = BuildTreeFromCodeTable(codeTable)
    
    #Create a new dialog window with a canvas to display the tree.
    treeWindow = tk.Toplevel(rootUIElement)
    treeWindow.title("Huffman Tree")
    treeCanvas = tk.Canvas(treeWindow, width=1920, height=1080, bg="white")
    treeCanvas.pack(fill=tk.BOTH, expand=True)
    
    #Draw the tree starting at the center of the canvas.
    canvasWidth = 1920
    rootX = canvasWidth / 2
    rootY = 50
    initialOffset = 200
    DrawTree(treeCanvas, tree, rootX, rootY, initialOffset)