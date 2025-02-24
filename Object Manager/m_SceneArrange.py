"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US: Groups objects in the scene into categories under new null objects.
"""
import c4d
from c4d import gui
import redshift as rs  # Ensure Redshift is available, or remove if not needed

# Fallback: if c4d does not have OmographCloner, define it
if not hasattr(c4d, "OmographCloner"):
    c4d.OmographCloner = 1018544

# ------------------------------
# Popup Menu Section
# ------------------------------
def show_menu():
    entries = c4d.BaseContainer()
    icons = {
        10: "&i18171&",        # Icon for Lights
        11: "&i18165&",        # Icon for Geometry
        12: "&i18170&",        # Icon for Cameras
        13: "&i440000235&",     # Icon for Generators
        14: "&i" + str(c4d.Ospline) + "&",   # Icon for Splines
        15: "&i1052838&",        # Icon for All
        16: "&i1058521&"         # Icon for Empty Nulls
    }
    
    entries.SetString(15, icons[15] + " All")
    entries.SetString(10, icons[10] + " Lights")
    entries.SetString(11, icons[11] + " Geometry")
    entries.SetString(12, icons[12] + " Cameras")
    entries.SetString(13, icons[13] + " Generators")
    entries.SetString(14, icons[14] + " Splines")
    entries.SetString(16, icons[16] + " Empty Nulls")
    
    result = gui.ShowPopupDialog(cd=None, bc=entries, x=c4d.MOUSEPOS, y=c4d.MOUSEPOS, flags=c4d.POPUP_RIGHT)
    category = None
    if result == 15:
        category = "All"
    elif result == 10:
        category = "Lights"
    elif result == 11:
        category = "Geometry"
    elif result == 12:
        category = "Cameras"
    elif result == 13:
        category = "Generators"
    elif result == 14:
        category = "Splines"
    elif result == 16:
        category = "Empty Nulls"
    return category

# ------------------------------
# Grouping Code Section
# ------------------------------
def gather_objects(root):
    """Recursively gathers objects starting from 'root'."""
    objects = []
    while root:
        objects.append(root)
        if root.GetDown():
            objects += gather_objects(root.GetDown())
        root = root.GetNext()
    return objects

def get_or_create_null(doc, null_name, display_color):
    """Searches for a grouping null with the given name; creates one if not found."""
    existing = doc.SearchObject(null_name)
    if existing:
        existing.SetParameter(c4d.ID_BASELIST_ICON_FILE, "1052838", c4d.DESCFLAGS_SET_0)
        existing[c4d.ID_BASELIST_ICON_COLOR] = display_color
        return existing

    new_null = c4d.BaseObject(c4d.Onull)
    new_null.SetName(null_name)
    doc.InsertObject(new_null)
    doc.AddUndo(c4d.UNDOTYPE_NEW, new_null)
    new_null.SetParameter(c4d.ID_BASELIST_ICON_FILE, "1052838", c4d.DESCFLAGS_SET_0)
    new_null[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2
    new_null[c4d.ID_BASELIST_ICON_COLOR] = display_color
    new_null.Message(c4d.MSG_UPDATE)
    return new_null

def GetTopParent(obj, groupNulls):
    """
    Moves up the hierarchy from 'obj' until finding the highest object that
    is not one of the grouping nulls.
    """
    parent = obj.GetUp()
    while parent and (parent not in groupNulls):
        obj = parent
        parent = obj.GetUp()
    return obj

def branch_contains_cloner(obj):
    """
    Checks if the object or any of its parents is a cloner.
    """
    current = obj
    while current:
        if current.CheckType(c4d.OmographCloner):
            return True
        current = current.GetUp()
    return False

def rgb_to_vector(r, g, b):
    """Converts 0-255 RGB values to a c4d.Vector with components between 0 and 1."""
    return c4d.Vector(r / 255.0, g / 255.0, b / 255.0)

def group_scene(selected_category):
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo()

    groups = {}
    groups_info = {
        "All":        None,                      # No color for "All"
        "Lights":     rgb_to_vector(255, 255, 0),      # Yellow
        "Geometry":   rgb_to_vector(70, 250, 200),     # Turquoise
        "Cameras":    rgb_to_vector(255, 60, 80),       # Red
        "Generators": rgb_to_vector(108, 229, 130),     # Light Green
        "Splines":    rgb_to_vector(140, 220, 250),      # Light Blue
        "Empty Nulls": rgb_to_vector(200, 200, 200)      # Grey
    }
    groupNulls = []

    # Define types for splines and primitives
    spline_types = [
        c4d.Ospline,
        c4d.Osplinerectangle,
        c4d.Osplinetext,
        c4d.Osplineprimitive,
        c4d.Osplinestar,
        c4d.Osplinearc,
        c4d.Osplinecircle,
        c4d.Osplinehelix,
        c4d.Osplinenside,
        c4d.Osplinecycloid,
        c4d.Ospline4side,
        c4d.Osplineflower,
        c4d.Osplinecogwheel
    ]
    
    primitive_types = [
        c4d.Ocube,
        c4d.Osphere,
        c4d.Ocylinder,
        c4d.Ocone,
        c4d.Oplane,
        c4d.Opyramid,
        c4d.Otorus,
        c4d.Otube,
        c4d.Ocapsule,
        c4d.Ofractal,
        c4d.Odisc,
        c4d.Oplatonic,
        c4d.Ofigure,
        c4d.Opolygon,
        c4d.Osinglepoly,
        c4d.Obezier,
        c4d.Ooiltank,
    ]

    # Definition of known light types.
    light_types = [
        c4d.Olight,
        c4d.Orslight,
        c4d.Orsenvironment,
        c4d.Orssky
    ]

    # Gather all objects in the scene
    topLevel = doc.GetFirstObject()
    allObjects = gather_objects(topLevel)
    moved = set()

    for obj in allObjects:
        # Skip existing grouping nulls (they have names matching our groups_info)
        if obj.CheckType(c4d.Onull) and obj.GetName() in groups_info:
            continue

        group_key = None
        # Determine the category for the object
        if branch_contains_cloner(obj) or obj.CheckType(c4d.Ovolumebuilder):
            group_key = "Generators"
        elif obj.CheckType(c4d.Ocamera) or obj.CheckType(c4d.Orscamera):
            group_key = "Cameras"
        elif any(obj.CheckType(light_type) for light_type in light_types):
            group_key = "Lights"
        elif any(obj.CheckType(s) for s in spline_types):
            group_key = "Splines"
            # Debug message:
            print("Spline detected:", obj.GetName(), "Type:", obj.GetType())
        elif any(obj.CheckType(p) for p in primitive_types):
            group_key = "Geometry"
        elif obj.CheckType(c4d.Onull) and not obj.GetDown():
            group_key = "Empty Nulls"
        
        # If a specific category was chosen, skip objects that don't match it.
        if selected_category != "All" and group_key != selected_category:
            continue
        
        if group_key:
            if group_key not in groups:
                groups[group_key] = get_or_create_null(doc, group_key, groups_info[group_key])
                groupNulls.append(groups[group_key])
            group = groups[group_key]
        else:
            group = None

        if group:
            top = GetTopParent(obj, groupNulls)
            if id(top) in moved:
                continue

            oldParent = top.GetUp()
            if oldParent:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, oldParent)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, top)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, group)

            top.Remove()
            top.InsertUnder(group)
            moved.add(id(top))

    doc.EndUndo()
    c4d.EventAdd()

# ------------------------------
# Main Execution
# ------------------------------
def main():
    selected_category = show_menu()
    if selected_category is None:
        return
    group_scene(selected_category)

if __name__=='__main__':
    main()
