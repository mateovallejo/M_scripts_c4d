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
        self.SetTitle("Enter Skip Value")
        if self.GroupBegin(0, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=2):
            self.AddStaticText(0, c4d.BFH_LEFT, name="Skip Every:")
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

def isCtrlPressed():
    """
    Returns True if the CTRL key is pressed.
    """
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        if qualifier & c4d.QCTRL:
            return True
    return False

def main():
    doc = c4d.documents.GetActiveDocument()
    # Get active object
    active_obj = doc.GetActiveObject()
    if not active_obj:
        c4d.gui.MessageDialog('Please select a polygon object.')
        return
    
    # Check if it's a polygon object
    if not active_obj.IsInstanceOf(c4d.Opolygon):
        c4d.gui.MessageDialog('Selected object must be a polygon object.')
        return

    # Get skip value based on modifiers
    skip_value = 2  # Default skip value
    if isCtrlPressed():
        dlg = AskNumber(DLG_TYPE_INT, 2)
        dlg.Open(c4d.DLG_TYPE_MODAL)
        if dlg.userCancel or dlg.value is None:
            return
        skip_value = int(dlg.value)
        if skip_value < 1:
            skip_value = 1

    # Get vertex count and create selection tag
    vertex_count = active_obj.GetPointCount()
    sel_tag = c4d.BaseTag(c4d.Tpointselection)
    sel_tag.SetName(f"Skip {skip_value} Vertices")
    
    # Get the selection container and deselect all
    point_sel = sel_tag.GetBaseSelect()
    point_sel.DeselectAll()
    
    # Select vertices based on ALT key state
    start_index = 1 if isAltPressed() else 0
    for i in range(start_index, vertex_count, skip_value):
        point_sel.Select(i)
    
    # Insert tag and update
    active_obj.InsertTag(sel_tag)
    c4d.EventAdd()

if __name__ == '__main__':
    main()