"""
Author: Mateo Vallejo
Website:
Version: 1.1.0
Description-US:Copy display color from first to multiple selected object.
"""

import c4d

def main():
    doc = c4d.documents.GetActiveDocument()
    
    # Retrieve selected objects in selection order, including explicitly selected children.
    selected_objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN | c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    
    # Debug: Print the names of the selected objects in the correct order.
    print("Selected objects in proper order:")
    for obj in selected_objs:
        print(" -", obj.GetName())
    
    # Ensure at least two objects are selected (one source and one target).
    if not selected_objs or len(selected_objs) < 2:
        return
    
    # Use the first selected object as the source for the color.
    source_obj = selected_objs[0]
    source_color = source_obj[c4d.ID_BASEOBJECT_COLOR]
    
    doc.StartUndo()
    
    # Loop through the rest of the selected objects and copy the color.
    for obj in selected_objs[1:]:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        # Force the object to use its own display color.
        obj[c4d.ID_BASEOBJECT_USECOLOR] = True
        # Copy the color properties from the source object.
        obj[c4d.ID_BASEOBJECT_COLOR] = source_color
        obj[c4d.ID_MG_TRANSFORM_COLOR] = source_color
        # Set the icon colorize mode so the color is visible in the Object Manager.
        obj[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2
        
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
