"""
Author: Mateo Vallejo
Website:
Version: 1.0.1
Description-US: Moves each selected object up one position in the hierarchy.
"""
import c4d

def isAltPressed():
    """ Returns True if the ALT key is pressed. """
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        if qualifier & c4d.QALT:
            return True
    return False

def main():
    doc.StartUndo()  # Start undo recording

    # Get selected objects
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

    # Check if the Alt key is pressed
    alt_pressed = isAltPressed()

    # Process objects in order to maintain correct order when moving up
    for obj in selection:
        if alt_pressed:
            # Move the object to the first position in the current group
            parent = obj.GetUp()
            if parent is not None:
                first_child = parent.GetDown()
                if first_child is not None and first_child != obj:
                    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
                    obj.Remove()
                    obj.InsertBefore(first_child)
        else:
            prev_obj = obj.GetPred()  # Get the previous object in the list
            if prev_obj is not None:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
                # Remove the object from its current position
                obj.Remove()
                # Insert the object before the previous one
                obj.InsertBefore(prev_obj)

    doc.EndUndo()  # End undo recording
    c4d.EventAdd()  # Update the scene

if __name__=='__main__':
    main()