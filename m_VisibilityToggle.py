"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Toggle selected objects visibility On/Off.
"""

import c4d
from c4d import BaseObject

def toggle_visibility(obj):
    # Get the current visibility state
    render_visibility = obj.GetRenderMode()
    viewport_visibility = obj.GetEditorMode()

    # Toggle visibility
    if render_visibility == c4d.MODE_UNDEF:
        render_visibility = c4d.MODE_OFF
    else:
        render_visibility = c4d.MODE_UNDEF

    if viewport_visibility == c4d.MODE_UNDEF:
        viewport_visibility = c4d.MODE_OFF
    else:
        viewport_visibility = c4d.MODE_UNDEF

    # Set the new visibility state
    obj.SetRenderMode(render_visibility)
    obj.SetEditorMode(viewport_visibility)

def main():
    # Get the active document and selected objects
    doc = c4d.documents.GetActiveDocument()
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    # Start the undo process
    doc.StartUndo()

    # Toggle visibility for each selected object
    for obj in selected_objects:
        # Add an undo operation for the object's visibility state
        doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, obj)
        toggle_visibility(obj)

    # End the undo process
    doc.EndUndo()

    # Update the scene
    c4d.EventAdd()

if __name__ == '__main__':
    main()
