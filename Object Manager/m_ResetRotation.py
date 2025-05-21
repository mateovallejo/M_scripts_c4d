"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Resets the rotation of each selected object to zero.
"""
import c4d
from c4d import gui

def main():
    # Start an undo action
    doc.StartUndo()

    # Get the selected objects
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    # Iterate over the selected objects and set the rotation to 0
    for obj in selected_objects:
        # Add undo for the rotation change
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_X] = 0
        obj[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Y] = 0
        obj[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Z] = 0

    # Record keyframes for all selected objects (Autokey support)
    if selected_objects:
        c4d.CallCommand(12410)  # Record Active Objects

    # End the undo action
    doc.EndUndo()

    # Update the scene
    c4d.EventAdd()

if __name__ == '__main__':
    main()