"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US: Make selected objects children of the last selected object.
"""

import c4d

def main():
    doc = c4d.documents.GetActiveDocument()

    # Retrieve selected objects in selection order if available
    if hasattr(c4d, 'GETACTIVEOBJECTFLAGS_SELECTIONORDER'):
        selected_objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    else:
        selected_objs = doc.GetActiveObjects(0)
    
    # Ensure we have at least two objects to reparent
    if not selected_objs or len(selected_objs) < 2:
        return

    # The last selected object becomes the parent
    parent_obj = selected_objs[-1]

    # Start recording undo steps
    doc.StartUndo()
    
    # For each object except the last one:
    for obj in selected_objs[:-1]:
        # Store the object's global transformation matrix
        mg = obj.GetMg()

        # Record the object's state for undo
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        
        # Reparent the object under the new parent
        obj.InsertUnder(parent_obj)
        
        # Compute the new local matrix such that:
        # new_local = old_global * inverse(new parent's global)
        # This preserves the object's world-space position/rotation/scale.
        new_ml = mg * ~parent_obj.GetMg()
        obj.SetMl(new_ml)

    # End undo recording and refresh Cinema 4D's scene
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
