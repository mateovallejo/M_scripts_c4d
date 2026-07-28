"""
Author: Mateo Vallejo
Website:
Version: 1.1.0
Description-US: Resets the position of each selected object to zero.
             - By default, resets the LOCAL/relative position to (0,0,0),
               i.e. the object snaps to its parent's origin (or world origin
               if it has no parent).
             - If the ALT key is pressed, resets the object's GLOBAL
               (world-space) position to (0,0,0) instead, regardless of
               parenting. Rotation and scale are left untouched either way.
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
    doc.StartUndo()

    # Get the selected objects
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    reset_to_world_origin = isAltPressed()

    # Iterate over the selected objects and set the position to 0
    for obj in selected_objects:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

        if reset_to_world_origin:
            # Reset GLOBAL position to world origin, keeping rotation/scale.
            # SetMg() correctly converts the desired global matrix into the
            # right local matrix for this object's parent (if any).
            mg = obj.GetMg()
            mg.off = c4d.Vector(0, 0, 0)
            obj.SetMg(mg)
        else:
            # Reset LOCAL/relative position (original behavior).
            obj[c4d.ID_BASEOBJECT_REL_POSITION, c4d.VECTOR_X] = 0
            obj[c4d.ID_BASEOBJECT_REL_POSITION, c4d.VECTOR_Y] = 0
            obj[c4d.ID_BASEOBJECT_REL_POSITION, c4d.VECTOR_Z] = 0

    # Record keyframes for all selected objects (Autokey support)
#    if selected_objects:
#        c4d.CallCommand(12410)  # Record Active Objects

    # Update the scene
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()