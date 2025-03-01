"""
Author: Mateo Vallejo
Website:
Version: 1.0.3
Name-US: m_AlignToLastSelected
Description-US: Align all selected objects to the last selected object's position and orientation.
"""

import c4d

def main():
    doc = c4d.documents.GetActiveDocument()
    
    # Retrieve selected objects in selection order if available
    if hasattr(c4d, 'GETACTIVEOBJECTFLAGS_SELECTIONORDER'):
        selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    else:
        selected = doc.GetActiveObjects(0)
    
    # Check that there are at least two selected objects
    if not selected or len(selected) < 2:
        print("Please select at least two objects")
        return

    # The last selected object is the target for alignment
    target_obj = selected[-1]
    
    doc.StartUndo()
    
    # For every object except the last one, align to the target's global matrix
    for obj in selected[:-1]:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj.SetMg(target_obj.GetMg())
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
