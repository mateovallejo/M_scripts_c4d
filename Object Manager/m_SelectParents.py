import c4d

def main():
    # Get the active document
    doc = c4d.documents.GetActiveDocument()
    
    # Get all selected objects
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    
    if not selected_objects:
        c4d.gui.MessageDialog("Please select at least one object.")
        return
    
    # Deselect all objects first
    doc.StartUndo()
    
    # Select parent objects
    for obj in selected_objects:
        parent = obj.GetUp()
        if parent:
            parent.SetBit(c4d.BIT_ACTIVE)
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
