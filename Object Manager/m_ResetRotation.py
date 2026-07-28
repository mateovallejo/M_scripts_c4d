"""
Author: Mateo Vallejo
Website:
Version: 1.1.0
Description-US: Resets the rotation of each selected object to zero.
             - By default, resets the LOCAL/relative rotation to (0,0,0),
               i.e. the object's rotation matches its parent's orientation
               (or world orientation if it has no parent).
             - If the ALT key is pressed, resets the object's GLOBAL
               (world-space) rotation to (0,0,0) instead, regardless of
               parenting. Position and scale are left untouched either way.
"""
import c4d
from c4d import gui

def isAltPressed():
    """
    Returns True if the ALT key is pressed.
    """
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        if qualifier & c4d.QALT:
            return True
    return False

def main():
    doc = c4d.documents.GetActiveDocument()

    # Start an undo action
    doc.StartUndo()

    # Get the selected objects
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    reset_to_world_rotation = isAltPressed()

    # Iterate over the selected objects and set the rotation to 0
    for obj in selected_objects:
        # Add undo for the rotation change
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

        if reset_to_world_rotation:
            # Reset GLOBAL rotation to world-aligned axes, keeping position
            # and scale. We rebuild the matrix from unit axes scaled by the
            # object's current global scale (assumes no skew, which covers
            # standard, non-sheared transforms).
            mg = obj.GetMg()
            scale = c4d.Vector(mg.v1.GetLength(), mg.v2.GetLength(), mg.v3.GetLength())
            new_mg = c4d.Matrix()
            new_mg.off = mg.off
            new_mg.v1 = c4d.Vector(scale.x, 0, 0)
            new_mg.v2 = c4d.Vector(0, scale.y, 0)
            new_mg.v3 = c4d.Vector(0, 0, scale.z)
            obj.SetMg(new_mg)
        else:
            # Reset LOCAL/relative rotation (original behavior).
            obj[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_X] = 0
            obj[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Y] = 0
            obj[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Z] = 0

    # Record keyframes for all selected objects (Autokey support)
#    if selected_objects:
#        c4d.CallCommand(12410)  # Record Active Objects

    # End the undo action
    doc.EndUndo()

    # Update the scene
    c4d.EventAdd()

if __name__ == '__main__':
    main()