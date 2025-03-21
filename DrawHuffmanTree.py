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

def LayoutTree(tree, depth, xCounter, positions):
    #This recursively computes a clean layout for the binary tree
    #We will use an in-order traversal to assign x cords to each node

    left = tree.get('0')
    right = tree.get('1')

    #If we have a leaf node, assign current x and increment counter
    if left is None and right is None:
        x = xCounter[0]
        positions[id(tree)] = (x, depth)
        xCounter[0] += 1
        return x
    else:
        #Process left child if it exists
        leftX = LayoutTree(left, depth + 1, xCounter, positions) if left is not None else None
        #Process right child if it exists
        rightX = LayoutTree(right, depth + 1, xCounter, positions) if right is not None else None
        #Compute the parent's x as the avg of its children
        if leftX is not None and rightX is not None:
            x = (leftX + rightX) / 2
        elif leftX is not None:
            x = leftX
        elif rightX is not None:
            x = rightX
        else:
            x = xCounter[0]
            xCounter[0] += 1

        positions[id(tree)] = (x, depth)
        return x
    
def DrawTreeWithPositions(canvas, tree, positions, margin, hSpacing, vSpacing, radius=20):
    #This function will draw the tree using precomputed positions

    #Define colors for various elements
    nodeFillColor = "#add8e6"      #Light blue for node fill
    nodeOutlineColor = "#000080"   #Navy blue for node outline
    textColor = "#000000"          #Black for node text
    edgeColor = "#008000"          #Green for connecting lines
    branchLabelColor = "#ff4500"   #OrangeRed for branch labels

    xLogical, depth = positions[id(tree)]
    x = margin + xLogical * hSpacing
    y = margin + depth * vSpacing

    #Leaf node
    label = tree.get('char', '')
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=nodeFillColor, outline=nodeOutlineColor, width=2)
    canvas.create_text(x, y, text=label, fill=textColor, font=("Helvetica", 12, "bold"))

    for bit in ['0', '1']:
        if bit in tree:
            child = tree[bit]
            childXLogical, childDepth = positions[id(child)]
            childX = margin + childXLogical * hSpacing
            childY = margin + childDepth * vSpacing
            #Draw line from parent's bottom to child's top.
            canvas.create_line(x, y + radius, childX, childY - radius, fill=edgeColor, width=2)
            #Label the line with the branch bit.
            mid_x = (x + childX) / 2
            mid_y = (y + childY) / 2
            canvas.create_text(mid_x, mid_y, text=bit, fill=branchLabelColor, font=("Helvetica", 10, "bold"))
            #Recursively draw the child node.
            DrawTreeWithPositions(canvas, child, positions, margin, hSpacing, vSpacing, radius)

def ComputeAndDrawTree(canvas, tree):
    #First this computes the tree's layout
    #then this draws it
    positions = {}
    xCounter = [0]
    LayoutTree(tree, 0, xCounter, positions)
    
    #Set desired spacing parameters.
    margin = 50
    hSpacing = 50   #horizontal distance per in-order unit
    vSpacing = 100  #vertical spacing per level

    #Determine the maximum extents from the positions.
    maxX = max(pos[0] for pos in positions.values())
    maxDepth = max(pos[1] for pos in positions.values())

    #Adjust the canvas scrollregion based on the drawing dimensions.
    canvas.config(scrollregion=(0, 0, margin + (maxX + 1) * hSpacing, margin + (maxDepth + 1) * vSpacing))
    
    #Clear the canvas before drawing.
    canvas.delete("all")
    
    #Draw the tree using the computed positions.
    DrawTreeWithPositions(canvas, tree, positions, margin, hSpacing, vSpacing)


def ShowHuffmanTree(codeTable, rootUIElement):
    #DO ALL VALIDATION BEFORE CALLING THIS FUNCTION
    #This function will take in a code table (straight from the .bin file)
    #and the root UI element

    tree = BuildTreeFromCodeTable(codeTable)
    
    #Create a new dialog window with a canvas to display the tree.
    treeWindow = tk.Toplevel(rootUIElement)
    treeWindow.title("Huffman Tree")
    treeWindow.attributes('-zoomed', True)

    #Create a frame to hold the canvas and scrollbars.
    frame = tk.Frame(treeWindow)
    frame.pack(fill=tk.BOTH, expand=True)

    #Create the canvas with an initially large scrollable region.
    treeCanvas = tk.Canvas(frame, bg="white", scrollregion=(0, 0, 5000, 5000))
    treeCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    #Add vertical and horizontal scrollbars.
    vbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=treeCanvas.yview)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    hbar = tk.Scrollbar(treeWindow, orient=tk.HORIZONTAL, command=treeCanvas.xview)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)

    #Configure the canvas to use the scrollbars.
    treeCanvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

    #Enable click-and-drag panning.
    def onButtonPress(event):
        treeCanvas.scan_mark(event.x, event.y)

    def onMouseDrag(event):
        treeCanvas.scan_dragto(event.x, event.y, gain=1)

    treeCanvas.bind("<ButtonPress-1>", onButtonPress)
    treeCanvas.bind("<B1-Motion>", onMouseDrag)

    #Compute the layout and draw the tree.
    ComputeAndDrawTree(treeCanvas, tree)

    #Update the window.
    treeWindow.update()

