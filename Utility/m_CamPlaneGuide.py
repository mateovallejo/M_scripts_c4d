"""
AR_AspectRatioGuide_Plane

Creates an aspect ratio guide as a Plane object for selected camera(s).
This is a copy of AR_AspectRatioGuide but uses a Plane instead of a Rectangle spline.

Author: Adapted from Arttu Rautio (aturtur) by assistant
Version: 1.0.0
"""

import c4d
from c4d import utils as u

# Functions (reused from original script)
def CreateUserDataLink(obj, name, link, parentGroup=None, shortname=None):
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BASELISTLINK)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_DEFAULT] = link
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
    bc[c4d.DESC_SHADERLINKFLAG] = True
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup

    element = obj.AddUserData(bc)
    obj[element] = link
    return element

def CreateUserDataCycle(obj, name, val, parentGroup=None, unit=c4d.DESC_UNIT_LONG):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_LONG)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_CYCLEBUTTON

    cycleBC = c4d.BaseContainer()
    items = val.split(',')
    for i, item in enumerate(items):
        cycleBC.SetString(i, item)

    bc[c4d.DESC_CYCLE] = cycleBC

    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup

    element = obj.AddUserData(bc)
    #obj[element] = val
    return element

def CreateUserDataFloat(obj, name, val=1.778, parentGroup=None, unit=c4d.DESC_UNIT_FLOAT):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REAL
    bc[c4d.DESC_MIN] = 0
    bc[c4d.DESC_MAX] = 1000
    bc[c4d.DESC_MINSLIDER] = 0
    bc[c4d.DESC_MAXSLIDER] = 1000
    bc[c4d.DESC_STEP] = 0.001
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateUserDataStaticText(obj, name, val="", parentGroup=None):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_STRING)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_STATICTEXT
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateUserDataButton(obj, name, parentGroup=None):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BUTTON)
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_BUTTON
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    return element

def CreateUserDataGroup(obj, name, parentGroup=None, columns=None, shortname=None):
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_GROUP)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_TITLEBAR] = False
    bc[c4d.DESC_GUIOPEN] = False
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    if columns is not None:
        bc[c4d.DESC_COLUMNS] = columns
    return obj.AddUserData(bc)

def CreateAspectRatioGuide_Plane(cam):
    # Create a Plane object instead of rectangle spline
    plane = c4d.BaseObject(c4d.Oplane)
    plane.SetName("Aspect Ratio Guide (Plane)")
    pyTag = c4d.BaseTag(1022749)
    pyTag.SetName("Aspect Ratio Guide Python Tag")

    CreateUserDataLink(pyTag, "Camera", None)
    CreateUserDataCycle(pyTag, "Presets", "9:16,3:5,2:3,4:5,1:1,5:4,4:3,5:3,16:9,1.85,21:9,2.35,2.39")
    CreateUserDataFloat(pyTag, "Aspect Ratio", 1.778)
    CreateUserDataFloat(pyTag, "Scale", 1.0)
    CreateUserDataStaticText(pyTag, "Width")
    CreateUserDataStaticText(pyTag, "Height")
    btnGroup = CreateUserDataGroup(pyTag, "Buttons", None, 2)
    CreateUserDataButton(pyTag, "Get Current", btnGroup)
    CreateUserDataButton(pyTag, "Crop", btnGroup)

    pyTag[c4d.ID_USERDATA,1] = cam

    plane.InsertTag(pyTag)
    plane.InsertUnder(cam)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, plane)

    m = cam.GetMg()
    m.off = m * c4d.Vector(0,0,100)
    plane.SetMg(m)
    # Ensure the plane primitive's axis is +Z (PRIM_AXIS = 4)
    try:
        plane[c4d.PRIM_AXIS] = 4
    except Exception:
        # Some C4D Python environments may not expose the same keys during static analysis;
        # ignore if we can't set it here — runtime in C4D will accept the assignment.
        pass

    # -------------------------------------------------------
    # The python tag code is largely the same as the rectangle
    # version but uses plane width/height primitive IDs.
    pyTag[c4d.TPYTHON_CODE] = """# Aspect Ratio Guide (Python Tag) - Plane version
import c4d
import math

def getFocalLength(old, new, focalLength):
    return (old / new) * focalLength

def getSensorSize(old, new, sensor):
    return sensor * (new / old)

def getFilmAnchor(old, new, current):
    return current * (old / new)

def getFilmOffset(old, new):
    filmOffset = ((1.0 - (old / new)) / 2.0)
    return filmOffset

def resizeComposition(camera, newWidth, newHeight):
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo()
    renderData = doc.GetActiveRenderData()
    focalLength = camera[c4d.CAMERA_FOCUS]
    sensorSize = camera[c4d.CAMERAOBJECT_APERTURE]
    zoom = camera[c4d.CAMERA_ZOOM]
    oldWidth = float(renderData[c4d.RDATA_XRES])
    oldHeight = float(renderData[c4d.RDATA_YRES])
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, camera)
    oldFilmOffsetY = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y])
    oldFilmOffsetX = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_X])
    camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(float(oldWidth), float(newWidth), sensorSize)
    camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(float(oldHeight), float(newHeight), oldFilmOffsetY)
    camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(float(oldWidth), float(newWidth), oldFilmOffsetX)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderData)
    renderData[c4d.RDATA_XRES]       = float(newWidth)
    renderData[c4d.RDATA_YRES]       = float(newHeight)
    renderData[c4d.RDATA_FILMASPECT] = float(newWidth) / float(newHeight)
    doc.SetActiveRenderData(renderData)
    doc.EndUndo()
    return True

def message(id, data):
    doc = c4d.documents.GetActiveDocument()
    renderData = doc.GetActiveRenderData()
    if id == c4d.MSG_DESCRIPTION_COMMAND:
        id2 = data['id'][0].id
        if id2 == c4d.ID_USERDATA:
            userDataId = data['id'][1].id
            if userDataId == 2:
                preset = op[c4d.ID_USERDATA,2]
                # ... same preset handling as original ...
                if preset == 0:
                    op[c4d.ID_USERDATA,3] = 0.5625
                elif preset == 1:
                     op[c4d.ID_USERDATA,3] = 0.6
                elif preset == 2:
                     op[c4d.ID_USERDATA,3] = 0.6666666666666666
                elif preset == 3:
                     op[c4d.ID_USERDATA,3] = 0.8
                elif preset == 4:
                     op[c4d.ID_USERDATA,3] = 1
                elif preset == 5:
                     op[c4d.ID_USERDATA,3] = 1.25
                elif preset == 6:
                     op[c4d.ID_USERDATA,3] = 1.3333333333333333
                elif preset == 7:
                     op[c4d.ID_USERDATA,3] = 1.6666666666666667
                elif preset == 8:
                     op[c4d.ID_USERDATA,3] = 1.7777777777777777
                elif preset == 9:
                     op[c4d.ID_USERDATA,3] = 1.85
                elif preset == 10:
                     op[c4d.ID_USERDATA,3] = 2.3333333333333335
                elif preset == 11:
                     op[c4d.ID_USERDATA,3] = 2.35
                elif preset == 12:
                     op[c4d.ID_USERDATA,3] = 2.39

            if userDataId == 8: # Get current aspect ratio
                doc.StartUndo()
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, op)
                op[c4d.ID_USERDATA,3] = renderData[c4d.RDATA_FILMASPECT]
                doc.EndUndo()
                c4d.EventAdd()

            if userDataId == 9: # Crop
                resizeComposition(op[c4d.ID_USERDATA,1], op[c4d.ID_USERDATA,5], op[c4d.ID_USERDATA,6])
                c4d.EventAdd()

def main():
    doc = c4d.documents.GetActiveDocument()
    renderData = doc.GetActiveRenderData()
    width = float(renderData[c4d.RDATA_XRES])
    height = float(renderData[c4d.RDATA_YRES])
    obj     = op.GetObject()
    presets = op[c4d.ID_USERDATA,2]
    cam     = op[c4d.ID_USERDATA,1]
    if cam == None: return False
    new_ar  = op[c4d.ID_USERDATA,3]
    scale   = op[c4d.ID_USERDATA,4]
    fov_ver = cam[c4d.CAMERAOBJECT_FOV_VERTICAL]
    fov_hor = cam[c4d.CAMERAOBJECT_FOV]
    zoom    = cam[c4d.CAMERA_ZOOM]
    film_x  = cam[c4d.CAMERAOBJECT_FILM_OFFSET_X]
    film_y  = cam[c4d.CAMERAOBJECT_FILM_OFFSET_Y]
    d       = obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z]

    fv = math.tan((fov_ver * 0.5)) * 2.0
    fh = math.tan((fov_hor * 0.5)) * 2.0
    h  = d * fv
    w  = d * fh

    pos_x = w * film_x
    pos_y = h * film_y * -1

    old_ar = width / height
    if old_ar > new_ar:
        w2 = h * new_ar
        h2 = h
        new_w = round((height * new_ar),2)
        new_h = round(height, 2)

    elif old_ar < new_ar:
        w2 = w
        h2 = w / new_ar
        new_w = round(width * 1, 2)
        new_h = round((width / new_ar),2)

    else:
        w2 = w
        h2 = h
        new_w = round(width, 2)
        new_h = round(height, 2)

    op[c4d.ID_USERDATA,5] = str(round(new_w*scale, 2))
    op[c4d.ID_USERDATA,6] = str(round(new_h*scale, 2))

    # Set plane width/height (primitive IDs for Plane)
    try:
        obj[c4d.PRIM_PLANE_WIDTH]  = w2 * scale
        obj[c4d.PRIM_PLANE_HEIGHT] = h2 * scale
    except Exception:
        # Fallback for older/newer API differences: use string keys
        obj["width"]  = w2 * scale
        obj["height"] = h2 * scale

    obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = pos_x
    obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = pos_y

    pass
"""

    pyTag.SetBit(c4d.BIT_ACTIVE)

    return True

def main():
    doc.StartUndo()

    selection = doc.GetActiveObjects(1)
    if len(selection) != 0:
        for s in selection:
            if (s.GetType() == 5103) or (s.GetType() == 1057516):
                CreateAspectRatioGuide_Plane(s)
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
                if s.GetNBit(c4d.NBIT_OM1_FOLD) == 0:
                    s.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_TOGGLE)
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
                s.DelBit(c4d.BIT_ACTIVE)
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
