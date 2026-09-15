"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US: Adds a Target tag to the selected object and links it to a new Null created at the scene origin.
"""

import c4d
import random

def isAltPressed():
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(
        c4d.BFM_INPUT_KEYBOARD,
        c4d.BFM_INPUT_CHANNEL,
        bc
    ):
        return bool(bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT)
    return False

def RandomValue(): # OLD
    r = random.random() # Random float
    return r # Return random float value


def RandomValueC():
    
    return min(random.random(), .7) # Limited

def main():
    doc = c4d.documents.GetActiveDocument()

    objects = doc.GetActiveObjects(
        c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER
    )

    if isAltPressed():
        if len(objects) < 2:
            c4d.gui.MessageDialog(
                "Select at least two objects in order."
            )
            return

        source = objects[0]
        target = objects[1]

        doc.StartUndo()

        targetTag = c4d.BaseTag(5676)
        if targetTag is None:
            doc.EndUndo()
            c4d.gui.MessageDialog("Could not create the Target tag.")
            return

        source.InsertTag(targetTag)
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, targetTag)

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, targetTag)
        targetTag[c4d.TARGETEXPRESSIONTAG_LINK] = target

        doc.EndUndo()
        c4d.EventAdd()
        return


    # Get the active (selected) object
    obj = doc.GetActiveObject()
    if obj is None:
        c4d.gui.MessageDialog("Please select at least one object.")
        return

    doc.StartUndo()

    # Create the Target Expression tag directly (plugin ID 5676) and insert it
    targetTag = c4d.BaseTag(5676)  # c4d.Ttargetexpression
    if targetTag is None:
        c4d.gui.MessageDialog("Could not create the Target tag.")
        doc.EndUndo()
        return

    obj.InsertTag(targetTag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, targetTag)

    # Create a Null object at the scene origin
    color = c4d.Vector(RandomValueC(), RandomValueC(), RandomValueC()) # Random color
    nullObj = c4d.BaseObject(c4d.Onull)
    nullObj.SetName(obj.GetName() + "_Target")
    nullObj[c4d.NULLOBJECT_DISPLAY] = 10
    nullObj[c4d.ID_BASEOBJECT_USECOLOR] = 2
    nullObj[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2
    nullObj[c4d.ID_BASEOBJECT_COLOR] = color
    nullObj[c4d.ID_BASELIST_ICON_COLOR] = color
    doc.InsertObject(nullObj)
    doc.AddUndo(c4d.UNDOTYPE_NEW, nullObj)

    # Link the new Null to the Target tag
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, targetTag)
    targetTag[c4d.TARGETEXPRESSIONTAG_LINK] = nullObj

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()