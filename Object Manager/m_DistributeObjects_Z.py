"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US: Distribute selected objects along the Z-axis ALT: Input gap value.
"""

import c4d

# Defines constants to know if the dialog ask an integer or a float
DLG_TYPE_FLOAT = 1
DLG_TYPE_INT = 2

class AskNumber(c4d.gui.GeDialog):
    ID_EDIT_NUMBER = 10000

    def __init__(self, dlgType=DLG_TYPE_FLOAT, value=0.0):
        if dlgType != DLG_TYPE_FLOAT and dlgType != DLG_TYPE_INT:
            raise ValueError("dlgType is not DLG_TYPE_FLOAT or DLG_TYPE_INT.")
        if dlgType == DLG_TYPE_FLOAT:
            try:
                value = float(value)
            except ValueError:
                raise ValueError("value should be convertible to float if DLG_TYPE_FLOAT is passed.")
        if dlgType == DLG_TYPE_INT:
            try:
                value = int(value)
            except ValueError:
                raise ValueError("value should be convertible to int if DLG_TYPE_INT is passed.")
        self.dlgType = dlgType
        self.defaultValue = value
        self.value = None
        self.userCancel = False

    def AskClose(self):
        if self.value is None and not self.userCancel:
            return True
        return False

    def CreateLayout(self):
        self.SetTitle("Enter a Number")
        if self.GroupBegin(0, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=2):
            self.AddStaticText(0, c4d.BFH_LEFT, name="Gap Value:")
            self.AddEditNumberArrows(self.ID_EDIT_NUMBER, c4d.BFH_SCALEFIT)
        self.GroupEnd()
        self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)
        return True

    def InitValues(self):
        if self.dlgType == DLG_TYPE_INT:
            self.SetInt32(self.ID_EDIT_NUMBER, int(self.defaultValue))
        elif self.dlgType == DLG_TYPE_FLOAT:
            self.SetFloat(self.ID_EDIT_NUMBER, float(self.defaultValue), step=0.1)
        return True

    def Command(self, id, msg):
        if id == self.ID_EDIT_NUMBER and msg[c4d.BFM_ACTION_RESET]:
            if self.dlgType == DLG_TYPE_FLOAT:
                self.SetFloat(self.ID_EDIT_NUMBER, self.defaultValue)
            else:
                self.SetInt32(self.ID_EDIT_NUMBER, self.defaultValue)
        if id == c4d.DLG_OK:
            self.value = self.GetFloat(self.ID_EDIT_NUMBER)
            self.userCancel = False
            self.Close()
        elif id == c4d.DLG_CANCEL:
            self.value = None
            self.userCancel = True
            self.Close()
        return True

def isAltPressed():
    """
    Returns True if the ALT key is pressed.
    """
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        if qualifier & c4d.QALT:
            return True
    return False

def get_hierarchy_bbox_global(op):
    """
    Recursively calculates the global bounding box (min and max vectors)
    for an object including all its children.
    """
    center = op.GetMp()
    rad = op.GetRad()
    local_min = center - rad
    local_max = center + rad

    corners = [
        c4d.Vector(local_min.x, local_min.y, local_min.z),
        c4d.Vector(local_min.x, local_min.y, local_max.z),
        c4d.Vector(local_min.x, local_max.y, local_min.z),
        c4d.Vector(local_min.x, local_max.y, local_max.z),
        c4d.Vector(local_max.x, local_min.y, local_min.z),
        c4d.Vector(local_max.x, local_min.y, local_max.z),
        c4d.Vector(local_max.x, local_max.y, local_min.z),
        c4d.Vector(local_max.x, local_max.y, local_max.z)
    ]

    global_corners = [op.GetMg() * corner for corner in corners]

    bbox_min = c4d.Vector(global_corners[0].x, global_corners[0].y, global_corners[0].z)
    bbox_max = c4d.Vector(global_corners[0].x, global_corners[0].y, global_corners[0].z)
    for pt in global_corners:
        bbox_min.x = min(bbox_min.x, pt.x)
        bbox_min.y = min(bbox_min.y, pt.y)
        bbox_min.z = min(bbox_min.z, pt.z)
        bbox_max.x = max(bbox_max.x, pt.x)
        bbox_max.y = max(bbox_max.y, pt.y)
        bbox_max.z = max(bbox_max.z, pt.z)

    child = op.GetDown()
    while child:
        child_min, child_max = get_hierarchy_bbox_global(child)
        bbox_min.x = min(bbox_min.x, child_min.x)
        bbox_min.y = min(bbox_min.y, child_min.y)
        bbox_min.z = min(bbox_min.z, child_min.z)
        bbox_max.x = max(bbox_max.x, child_max.x)
        bbox_max.y = max(bbox_max.y, child_max.y)
        bbox_max.z = max(bbox_max.z, child_max.z)
        child = child.GetNext()

    return bbox_min, bbox_max

def main():
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo()

    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if not objs:
        doc.EndUndo()
        return

    # Determine if gap should be applied
    gap_enabled = isAltPressed()
    gap_value = 0.0
    if gap_enabled:
        dlg = AskNumber(DLG_TYPE_FLOAT, 10.0)
        dlg.Open(c4d.DLG_TYPE_MODAL)
        if dlg.userCancel or dlg.value is None:
            print("User canceled gap input. Exiting.")
            doc.EndUndo()
            return
        gap_value = dlg.value

    currentZ = 0.0

    for obj in objs:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        bbox_min, bbox_max = get_hierarchy_bbox_global(obj)
        offset = currentZ - bbox_min.z
        pos = obj.GetAbsPos() + c4d.Vector(0, 0, offset)
        obj.SetAbsPos(pos)
        currentZ = bbox_max.z + offset
        if gap_enabled:
            currentZ += gap_value

    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
