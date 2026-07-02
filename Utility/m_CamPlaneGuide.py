"""
m_CamPlaneGuide

Author: Mateo Vallejo
Website: https://mateovallejo.com
Name-US: m_CamPlaneGuide
Version: 1.0.0
Description-US: Creates a plane that matches render dimensions as child of selected camera(s)

Written for Maxon Cinema 4D 2025
Python version 3.9+

Change log:
1.0.0 (27.08.2025) - Initial release
"""

import c4d
import math

def CreateUserDataBool(obj, name, val=True, parentGroup=None):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BOOL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateUserDataFloat(obj, name, val=1.0, parentGroup=None, unit=c4d.DESC_UNIT_FLOAT):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REAL
    bc[c4d.DESC_MIN] = 0
    bc[c4d.DESC_MAX] = 10000
    bc[c4d.DESC_MINSLIDER] = 0
    bc[c4d.DESC_MAXSLIDER] = 10000
    bc[c4d.DESC_STEP] = 1
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateCameraGuide(cam, doc):
    # Create a plane object
    plane = c4d.BaseObject(c4d.Oplane)
    plane.SetName("Camera Guide")
    
    # Add python tag to control the plane
    pyTag = c4d.BaseTag(1022749)  # Python tag
    pyTag.SetName("Camera Guide Python Tag")
    
    # Create group for custom dimensions
    customGroup = c4d.BaseContainer()
    customGroup.SetBool(c4d.DESC_TITLEBAR, True)
    customGroup.SetString(c4d.DESC_NAME, "Custom Dimensions")
    customGroup.SetString(c4d.DESC_SHORT_NAME, "Custom Dimensions")
    customId = pyTag.AddUserData(customGroup)
    
    # Add user data
    CreateUserDataFloat(pyTag, "Scale", 1.0)
    CreateUserDataBool(pyTag, "Use Custom Dimensions", False, customId)
    CreateUserDataFloat(pyTag, "Width", 1920.0, customId)
    CreateUserDataFloat(pyTag, "Height", 1080.0, customId)
    
    # Insert the python tag
    plane.InsertTag(pyTag)
    
    # Make the plane a child of the camera
    plane.InsertUnder(cam)
    
    # Add to undo history
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, plane)
    
    # Position the plane 100 units in front of the camera
    m = cam.GetMg()
    m.off = m * c4d.Vector(0, 0, 100)
    plane.SetMg(m)
    
    # Add the Python script to control the plane
    pyTag[c4d.TPYTHON_CODE] = '''# Camera Guide (Python Tag)
import c4d
import math

def main():
    doc = c4d.documents.GetActiveDocument()
    renderData = doc.GetActiveRenderData()
    
    # Get objects
    obj = op.GetObject()
    cam = obj.GetUp()  # Get parent camera
    if not cam: return False
    
    # Get user data values
    scale = op[c4d.ID_USERDATA,1]  # Scale
    use_custom = op[c4d.ID_USERDATA,2]  # Use Custom Dimensions
    custom_width = op[c4d.ID_USERDATA,3]  # Custom Width
    custom_height = op[c4d.ID_USERDATA,4]  # Custom Height
    
    # Get dimensions
    if use_custom:
        width = float(custom_width)
        height = float(custom_height)
    else:
        width = float(renderData[c4d.RDATA_XRES])
        height = float(renderData[c4d.RDATA_YRES])
    
    # Get camera parameters
    fov_ver = cam[c4d.CAMERAOBJECT_FOV_VERTICAL]
    fov_hor = cam[c4d.CAMERAOBJECT_FOV]
    film_x = cam[c4d.CAMERAOBJECT_FILM_OFFSET_X]
    film_y = cam[c4d.CAMERAOBJECT_FILM_OFFSET_Y]
    d = obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z]
    
    # Calculate dimensions based on FOV
    fv = math.tan((fov_ver * 0.5)) * 2.0
    fh = math.tan((fov_hor * 0.5)) * 2.0
    h = d * fv
    w = d * fh
    
    # Adjust dimensions to match aspect ratio
    aspect = width / height
    if aspect > 1:
        w = h * aspect
    else:
        h = w / aspect
    
    # Calculate position offsets based on film offset
    pos_x = w * film_x
    pos_y = h * film_y * -1
    
    # Set plane size
    obj[c4d.PRIM_PLANE_WIDTH] = w * scale
    obj[c4d.PRIM_PLANE_HEIGHT] = h * scale
    
    # Set plane position
    obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = pos_x
    obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = pos_y
'''
    
    # Activate the tag
    pyTag.SetBit(c4d.BIT_ACTIVE)
    return True

def main():
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo()
    
    # Get selected cameras
    selection = doc.GetActiveObjects(1)
    if len(selection) != 0:
        for s in selection:
            # Check if object is a C4D camera or Redshift camera
            if (s.GetType() == 5103) or (s.GetType() == 1057516):
                CreateCameraGuide(s, doc)
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
                # Unfold camera in object manager if folded
                if s.GetNBit(c4d.NBIT_OM1_FOLD) == 0:
                    s.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_TOGGLE)
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
                s.DelBit(c4d.BIT_ACTIVE)
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
