"""
Copyright: MAXON Computer GmbH
Author: Manuel Magalhaes (modified by Assistant)

Description:
    - Copies the position, rotation, and animation Tracks (all Keyframes) from the first selected object to all other selected objects.
    - If a target object already has animation data for its position, rotation, or scale, that data will be removed before copying.

Notes:
    - Selection order is used: the first selected object is the source, and all subsequent selected objects are the targets.
"""

import c4d

def main():
    doc = c4d.documents.GetActiveDocument()
    
    # Retrieve selected objects in selection order if available.
    if hasattr(c4d, 'GETACTIVEOBJECTFLAGS_SELECTIONORDER'):
        selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    else:
        selected = doc.GetActiveObjects(0)
    
    # Check that there are at least two selected objects.
    if not selected or len(selected) < 2:
        c4d.gui.MessageDialog("Please select at least two objects")
        return

    # The first selected object is the source (with animation tracks).
    source_obj = selected[0]
    # The remaining objects are the targets.
    target_objs = selected[1:]
    
    # Retrieve all the CTracks from the source object.
    tracks = source_obj.GetCTracks()
    if not tracks:
        c4d.gui.MessageDialog("No animated tracks found on the source object.")
        return

    # Define a list of parameter IDs to copy.
    trackListToCopy = [
        c4d.ID_BASEOBJECT_REL_POSITION,
        c4d.ID_BASEOBJECT_REL_ROTATION,
        c4d.ID_BASEOBJECT_REL_SCALE
    ]

    doc.StartUndo()

    # Iterate over all target objects.
    for target_obj in target_objs:
        # For each track in the source object, process and copy if applicable.
        for track in tracks:
            did = track.GetDescriptionID()

            # Only copy if the parameter is in our list.
            if not did[0].id in trackListToCopy:
                continue

            # Remove any existing track on the target for this parameter.
            foundTrack = target_obj.FindCTrack(did)
            if foundTrack:
                doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, foundTrack)
                foundTrack.Remove()

            # Clone the track (including curves and keyframes) from the source.
            clone = track.GetClone()
            target_obj.InsertTrackSorted(clone)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, clone)

        # Update target object's geometry to reflect new keyframes.
        animateFlag = c4d.ANIMATEFLAGS_NONE if c4d.GetC4DVersion() > 20000 else c4d.ANIMATEFLAGS_0
        doc.AnimateObject(target_obj, doc.GetTime(), animateFlag)

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == "__main__":
    main()
