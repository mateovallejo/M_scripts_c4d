"""
Author: Mateo Vallejo
Website:
Version: 1.0.1
Name-US:m_AlignToSelected
Description-US:Align first selected object to second selected object.
"""

import c4d

def main():
    # Get the selected objects
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    # Check that there are at least two selected objects
    if len(selected) < 2:
        print("Please select at least two objects")
        return

    # Get the first and second selected objects
    first_obj = selected[0]
    second_obj = selected[1]

    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, first_obj)

    # Copy the coordinates from the second object to the first object
    first_obj.SetMg(second_obj.GetMg())

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, first_obj)
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()