"""
Author: Mateo Vallejo
Website:
Version: 1.0.2
Description-US:Copy display color from parent to children of selected objects.
"""

import c4d

def apply_color_to_children(parent_obj, color_use, color_value):
    # Get the children of the current object
    children = parent_obj.GetChildren()
    
    # Iterate over each child
    for child in children:
        # Register the state of the object before making changes
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)
        
        # Copy the display color property from the parent to the child
        child[c4d.ID_BASEOBJECT_USECOLOR] = color_use
        child[c4d.ID_BASEOBJECT_COLOR] = color_value
        child[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2  # Ensure the color is shown in the icon
        
        # Recursively call the function to process the descendants
        apply_color_to_children(child, color_use, color_value)

def main():
    # Get the selected objects
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    # Check that there is at least one selected object
    if not selected:
        c4d.gui.MessageDialog("Please select at least one object.")
        return

    doc.StartUndo()

    # Iterate over each selected object
    for parent_obj in selected:
        # Save the color properties of the parent object
        color_use = parent_obj[c4d.ID_BASEOBJECT_USECOLOR]
        color_value = parent_obj[c4d.ID_BASEOBJECT_COLOR]

        # Call the function to apply the color to all descendants
        apply_color_to_children(parent_obj, color_use, color_value)

    doc.EndUndo()
    c4d.EventAdd()

# Execute the main function
if __name__ == '__main__':
    main()
