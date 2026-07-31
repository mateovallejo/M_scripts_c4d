"""
Author: Mateo Vallejo
Website: http://mateovallejo.com/
Name-US: m_PyTagMatchChildrenColor
Version: 1.0.0
Description-US: Adds a custom python tag for selected object(s) that matches children's display color to the parent's
Written for Maxon Cinema 4D R25.117
Python version 3.9.1
Change log:
1.0.0 (31.07.2026) - First version
"""
# Libraries
import c4d
from c4d import utils as u

# Functions
def CreateUserDataCycle(obj, name, val, parentGroup=None, unit=c4d.DESC_UNIT_LONG):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_LONG)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_CYCLE
    cycleBC = c4d.BaseContainer()
    items = val.split(',')
    for i, item in enumerate(items):
        cycleBC.SetString(i, item)
    bc[c4d.DESC_CYCLE] = cycleBC
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    return element

def CreateUserDataBool(obj, name, val, parentGroup=None):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BOOL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_BOOL
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreatePythonTag(obj):
    pyTag = c4d.BaseTag(1022749)
    scriptPath = __file__
    iconPath = scriptPath.rsplit('.', 1)[0]+".tif"
    pyTag[c4d.ID_BASELIST_ICON_FILE] = iconPath
    pyTag.SetName("m_MatchChildrenColor")
    obj.InsertTag(pyTag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, pyTag)
    CreateUserDataCycle(pyTag, "Method", "Direct Children,Recursive")
    CreateUserDataBool(pyTag, "Force Use Color", True)
    # Python Tag code
    # -------------------------------------------------------
    pyTag[c4d.TPYTHON_CODE] = "# AR_MatchChildrenColor (Python Tag)\n\
# Author: Mateo Vallejo\n\
# Website: http://mateovallejo.com/\n\
# Version: 1.0.0\n\
\n\
# Libraries\n\
import c4d\n\
\n\
# Functions\n\
def SetChildColor(child, color, forceUseColor):\n\
    if forceUseColor:\n\
        child[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Always\n\
    child[c4d.ID_BASEOBJECT_COLOR] = color\n\
\n\
def CollectChildren(obj, recursive):\n\
    children = []\n\
    child = obj.GetDown()\n\
    while child is not None:\n\
        children.append(child)\n\
        if recursive:\n\
            children += CollectChildren(child, recursive)\n\
        child = child.GetNext()\n\
    return children\n\
\n\
def main():\n\
    obj = op.GetObject() # Get object\n\
    method = op[c4d.ID_USERDATA,1]\n\
    forceUseColor = op[c4d.ID_USERDATA,2]\n\
    color = obj[c4d.ID_BASEOBJECT_COLOR] # Parent's display color\n\
    recursive = (method == 1)\n\
    children = CollectChildren(obj, recursive)\n\
    for child in children:\n\
        SetChildColor(child, color, forceUseColor)\n\
    return True # All good"
    # -------------------------------------------------------
    return True # All good

def main():
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(1)
    if len(selection) != 0:
        for s in selection:
            CreatePythonTag(s) # Run the function
    doc.EndUndo() # Start recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()