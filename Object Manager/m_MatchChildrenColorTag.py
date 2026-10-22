"""
Author: Mateo Vallejo
Website: http://mateovallejo.com/
Name-US: m_PyTagLayerFromObject
Version: 1.0.0
Description-US: Adds a custom python tag for selected object(s) that creates a layer named after the object and assigns all its children to that layer
Written for Maxon Cinema 4D R25.117
Python version 3.9.1
"""
# Libraries
import c4d

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
    iconPath = scriptPath.rsplit('.', 1)[0] + ".tif"
    pyTag[c4d.ID_BASELIST_ICON_FILE] = iconPath
    pyTag.SetName("m_LayerFromObject")
    obj.InsertTag(pyTag)
    doc.AddUndo(c4d.UNDOTYPE_NEW, pyTag)
    CreateUserDataCycle(pyTag, "Method", "Recursive, Direct Children")  # ID 1
    CreateUserDataBool(pyTag, "Include Parent", True)                 # ID 2
    # Python Tag code
    # -------------------------------------------------------
    pyTag[c4d.TPYTHON_CODE] = r"""# m_LayerFromObject (Python Tag)
# Author: Mateo Vallejo
# Website: http://mateovallejo.com/
# Version: 1.0.0

# Libraries
import c4d

# Functions
def FindLayerByName(layer, name):
    # Search the layer hierarchy (recursively) for a layer with the given name
    while layer is not None:
        if layer.GetName() == name:
            return layer
        found = FindLayerByName(layer.GetDown(), name)
        if found is not None:
            return found
        layer = layer.GetNext()
    return None

def GetOrCreateLayer(doc, name):
    root = doc.GetLayerObjectRoot()
    layer = FindLayerByName(root.GetDown(), name)
    if layer is None:
        layer = c4d.documents.LayerObject()
        layer.SetName(name)
        layer.InsertUnder(root)
    return layer

def CollectChildren(obj, recursive):
    children = []
    child = obj.GetDown()
    while child is not None:
        children.append(child)
        if recursive:
            children += CollectChildren(child, recursive)
        child = child.GetNext()
    return children

def main():
    obj = op.GetObject()
    if obj is None:
        return

    method = op[c4d.ID_USERDATA, 1]
    includeParent = op[c4d.ID_USERDATA, 2]
    recursive = (method == 1)

    targets = CollectChildren(obj, recursive)
    if includeParent:
        targets.append(obj)

    # Nothing to do (avoids creating an empty layer for objects without children)
    if not targets:
        return

    layer = GetOrCreateLayer(doc, obj.GetName())

    changed = False
    for target in targets:
        if target.GetLayerObject(doc) != layer:
            target.SetLayerObject(layer)
            changed = True

    if changed:
        c4d.EventAdd()
"""
    # -------------------------------------------------------
    return True  # All good

def main():
    doc.StartUndo()  # Start recording undos
    selection = doc.GetActiveObjects(1)
    if len(selection) != 0:
        for s in selection:
            CreatePythonTag(s)  # Run the function
    doc.EndUndo()  # Stop recording undos
    c4d.EventAdd()  # Update Cinema 4D

# Execute main()
if __name__ == '__main__':
    main()