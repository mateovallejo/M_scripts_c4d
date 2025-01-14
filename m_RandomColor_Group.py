"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Set same random display color to current object selection.
"""


import c4d
import random

def RandomValue():
    r = random.random() # Random float
    return r # Return random float value

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos


    try: # Try to execute following script
        selection = doc.GetActiveObjects(1) # Get object selection
        if len(selection) == 0:
            return # If nothing is selected, exit

        # Generate a single random color
        color = c4d.Vector(RandomValue(), RandomValue(), RandomValue()) # Random color

        for obj in selection: # Iterate through selected objects
            doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, obj) # Record undo
            obj[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Display Color = On
            obj[c4d.ID_BASEOBJECT_COLOR] = color # Apply the same random color to all objects
            obj[c4d.ID_MG_TRANSFORM_COLOR] = color # Apply the same random color to cloner object
            obj[c4d.ID_BASELIST_ICON_COLOR] = color # Apply the same random color to icon color
            obj[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2

    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()