"""
Author: Mateo Vallejo
Website:
Version: 1.0.1
Description-US:Copy display color from first to second selected object.
"""

import c4d

def main():
    # Get all selected elements
    selection = doc.GetSelection()

    # Filter only objects (exclude tags, materials, etc.)
    selected = [s for s in selection if isinstance(s, c4d.BaseObject)]

    # Get the first and second selected objects
    first_obj = selected[0]
    second_obj = selected[1]

    # Start the undo operation
    doc.StartUndo()

    # Register the state of the object before making changes
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, second_obj)

    # Copy the display color property from the first object to the second
    second_obj[c4d.ID_BASEOBJECT_USECOLOR] = first_obj[c4d.ID_BASEOBJECT_USECOLOR]
    second_obj[c4d.ID_BASEOBJECT_COLOR] = first_obj[c4d.ID_BASEOBJECT_COLOR]
    second_obj[c4d.ID_MG_TRANSFORM_COLOR] = first_obj[c4d.ID_BASEOBJECT_COLOR]
    second_obj[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2

    # End the undo operation
    doc.EndUndo()

    # Refresh the document to see the changes
    c4d.EventAdd()

# Execute the main function
if __name__=='__main__':
    main()