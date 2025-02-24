"""
Author: Mateo Vallejo
Website:
Version: 1.0.1
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

    if not selected_objs or len(selected_objs) < 2:
        return

    # The last selected object becomes the parent.
    parent_obj = selected_objs[-1]
    # Store the parent's global matrix before changing the hierarchy.
    parent_mg = parent_obj.GetMg()

    doc.StartUndo()

    for obj in selected_objs[:-1]:
        mg = obj.GetMg()
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj.InsertUnder(parent_obj)
        obj.SetMg(mg)

    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()