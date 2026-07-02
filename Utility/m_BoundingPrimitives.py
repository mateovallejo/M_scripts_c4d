"""
Author: Mateo Vallejo
Website: https://mateovallejo.com
Version: 1.3.5
Description: Creates a primitive that matches the bounding box dimensions of selected objects,
             with axis orientation selection. Sphere rotated for axis simulation. Pyramid fixed.
"""

import c4d
from c4d import gui, Vector, utils

# -------------------------------
# Menu Helpers
# -------------------------------
def create_primitive_menu():
    primitives = {
        c4d.Ocube: "Box",
        c4d.Osphere: "Sphere",
        c4d.Ocylinder: "Cylinder",
        c4d.Ocone: "Cone",
        c4d.Opyramid: "Pyramid",
        c4d.Otube: "Tube",
        c4d.Ocapsule: "Capsule"
    }
    entries = c4d.BaseContainer()
    menu_map = {}
    menu_id = 1000
    for pid, name in primitives.items():
        entries.SetString(menu_id, name)
        menu_map[menu_id] = pid
        menu_id += 1
    res = gui.ShowPopupDialog(cd=None, bc=entries,
                              x=c4d.MOUSEPOS, y=c4d.MOUSEPOS,
                              flags=c4d.POPUP_RIGHT)
    return menu_map.get(res, None)

def create_axis_menu(primitive_type):
    axis_labels = {
        c4d.PRIM_AXIS_XP: "+X",
        c4d.PRIM_AXIS_XN: "-X",
        c4d.PRIM_AXIS_YP: "+Y",
        c4d.PRIM_AXIS_YN: "-Y",
        c4d.PRIM_AXIS_ZP: "+Z",
        c4d.PRIM_AXIS_ZN: "-Z"
    }
    if primitive_type in (c4d.Ocube, c4d.Osphere):
        axes = [c4d.PRIM_AXIS_XP, c4d.PRIM_AXIS_YP, c4d.PRIM_AXIS_ZP]
    else:
        axes = [
            c4d.PRIM_AXIS_XP, c4d.PRIM_AXIS_XN,
            c4d.PRIM_AXIS_YP, c4d.PRIM_AXIS_YN,
            c4d.PRIM_AXIS_ZP, c4d.PRIM_AXIS_ZN
        ]
    entries = c4d.BaseContainer()
    menu_map = {}
    menu_id = 2000
    for axis in axes:
        entries.SetString(menu_id, axis_labels[axis])
        menu_map[menu_id] = axis
        menu_id += 1
    res = gui.ShowPopupDialog(cd=None, bc=entries,
                              x=c4d.MOUSEPOS, y=c4d.MOUSEPOS,
                              flags=c4d.POPUP_RIGHT)
    return menu_map.get(res, None)

# -------------------------------
# Bounding Box Helpers
# -------------------------------
def calculate_bounding_box_objects(obj, min_point, max_point, ref_inv_mg=None):
    mp = obj.GetMp()
    rad = obj.GetRad()
    corners = [
        Vector(mp.x - rad.x, mp.y - rad.y, mp.z - rad.z),
        Vector(mp.x + rad.x, mp.y - rad.y, mp.z - rad.z),
        Vector(mp.x - rad.x, mp.y + rad.y, mp.z - rad.z),
        Vector(mp.x + rad.x, mp.y + rad.y, mp.z - rad.z),
        Vector(mp.x - rad.x, mp.y - rad.y, mp.z + rad.z),
        Vector(mp.x + rad.x, mp.y - rad.y, mp.z + rad.z),
        Vector(mp.x - rad.x, mp.y + rad.y, mp.z + rad.z),
        Vector(mp.x + rad.x, mp.y + rad.y, mp.z + rad.z)
    ]
    mg = obj.GetMg()
    for p in corners:
        p_global = mg * p
        p_local = ref_inv_mg * p_global if ref_inv_mg else p_global
        min_point = Vector(min(min_point.x, p_local.x),
                           min(min_point.y, p_local.y),
                           min(min_point.z, p_local.z))
        max_point = Vector(max(max_point.x, p_local.x),
                           max(max_point.y, p_local.y),
                           max(max_point.z, p_local.z))
    child = obj.GetDown()
    while child:
        min_point, max_point = calculate_bounding_box_objects(child, min_point, max_point, ref_inv_mg)
        child = child.GetNext()
    return min_point, max_point

def get_selected_points_from_selection(obj, mode):
    points = set()
    
    # Force only one type of sub-object selection based on the current mode
    if mode == c4d.Mpoints:
        obj.GetEdgeS().DeselectAll()
        obj.GetPolygonS().DeselectAll()
    elif mode == c4d.Medges:
        obj.GetPointS().DeselectAll()
        obj.GetPolygonS().DeselectAll()
    elif mode == c4d.Mpolygons:
        obj.GetPointS().DeselectAll()
        obj.GetEdgeS().DeselectAll()
        
    point_sel = obj.GetPointS()
    if mode == c4d.Mpoints and point_sel.GetCount() > 0:
        for i in range(obj.GetPointCount()):
            if point_sel.IsSelected(i):
                points.add(i)
        return points, 'points'
    edge_sel = obj.GetEdgeS()
    if mode == c4d.Medges and edge_sel.GetCount() > 0:
        polygons = obj.GetAllPolygons()
        for i in range(obj.GetPolygonCount()):
            poly = polygons[i]
            edges = [(poly.a, poly.b), (poly.b, poly.c),
                     (poly.c, poly.d if poly.c != poly.d else poly.a),
                     (poly.d, poly.a)]
            for j, edge in enumerate(edges):
                if edge_sel.IsSelected(4 * i + j):
                    points.update(edge)
        return points, 'edges'
    poly_sel = obj.GetPolygonS()
    if mode == c4d.Mpolygons and poly_sel.GetCount() > 0:
        for i in range(obj.GetPolygonCount()):
            if poly_sel.IsSelected(i):
                poly = obj.GetPolygon(i)
                points.update([poly.a, poly.b, poly.c, poly.d])
        return points, 'faces'
    return points, None

# -------------------------------
# Primitive Creation
# -------------------------------
def create_bounding_primitive(primitive_type, axis, min_point, max_point, doc, ref_mg=None):
    size = max_point - min_point
    center = (max_point + min_point) / 2
    primitive = c4d.BaseObject(primitive_type)

    # -------------------
    # Apply axis
    # -------------------
    if primitive_type != c4d.Osphere:
        primitive[c4d.PRIM_AXIS] = axis

    # -------------------
    # Dimension mapping
    # -------------------
    def get_height_radius(size, axis):
        if axis in (c4d.PRIM_AXIS_XP, c4d.PRIM_AXIS_XN):
            return size.x, max(size.y, size.z)/2
        elif axis in (c4d.PRIM_AXIS_YP, c4d.PRIM_AXIS_YN):
            return size.y, max(size.x, size.z)/2
        else:
            return size.z, max(size.x, size.y)/2

    if primitive_type == c4d.Ocube:
        primitive[c4d.PRIM_CUBE_LEN] = size
    elif primitive_type == c4d.Osphere:
        primitive[c4d.PRIM_SPHERE_RAD] = max(size.x, size.y, size.z)/2
    elif primitive_type == c4d.Ocylinder:
        h, r = get_height_radius(size, axis)
        primitive[c4d.PRIM_CYLINDER_HEIGHT] = h
        primitive[c4d.PRIM_CYLINDER_RADIUS] = r
    elif primitive_type == c4d.Ocone:
        h, r = get_height_radius(size, axis)
        primitive[c4d.PRIM_CONE_TRAD] = 0
        primitive[c4d.PRIM_CONE_BRAD] = r
        primitive[c4d.PRIM_CONE_HEIGHT] = h
    elif primitive_type == c4d.Opyramid:
        if axis in (c4d.PRIM_AXIS_XP, c4d.PRIM_AXIS_XN):
            primitive[c4d.PRIM_PYRAMID_LEN] = Vector(size.y, size.x, size.z)
        elif axis in (c4d.PRIM_AXIS_YP, c4d.PRIM_AXIS_YN):
            primitive[c4d.PRIM_PYRAMID_LEN] = size
        else:
            primitive[c4d.PRIM_PYRAMID_LEN] = Vector(size.x, size.z, size.y)
    elif primitive_type == c4d.Otube:
        h, r = get_height_radius(size, axis)
        primitive[c4d.PRIM_TUBE_HEIGHT] = h
        primitive[c4d.PRIM_TUBE_ORAD] = r
        primitive[c4d.PRIM_TUBE_IRAD] = r*0.8
    elif primitive_type == c4d.Ocapsule:
        h, r = get_height_radius(size, axis)
        primitive[c4d.PRIM_CAPSULE_HEIGHT] = h
        primitive[c4d.PRIM_CAPSULE_RADIUS] = r

    # -------------------
    # Apply rotation for sphere
    # -------------------
    if primitive_type == c4d.Osphere:
        rot = Vector(0,0,0)
        if axis in (c4d.PRIM_AXIS_XP, c4d.PRIM_AXIS_XN):
            rot.z = utils.DegToRad(90)
        elif axis in (c4d.PRIM_AXIS_ZP, c4d.PRIM_AXIS_ZN):
            rot.x = utils.DegToRad(90)
        primitive.SetRelRot(rot)

    # -------------------
    # Apply global matrix
    # -------------------
    if ref_mg:
        mg = c4d.Matrix(center, c4d.Vector(1,0,0), c4d.Vector(0,1,0), c4d.Vector(0,0,1))
        primitive.SetMg(ref_mg * mg)
    else:
        primitive.SetAbsPos(center)

    doc.InsertObject(primitive)
    doc.AddUndo(c4d.UNDOTYPE_NEW, primitive)
    return primitive

# -------------------------------
# Main
# -------------------------------
def main():
    primitive_type = create_primitive_menu()
    if not primitive_type:
        return
    axis = create_axis_menu(primitive_type)
    if axis is None:
        return

    doc = c4d.documents.GetActiveDocument()
    mode = doc.GetMode()
    doc.StartUndo()

    if mode == c4d.Mmodel:
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if not selection:
            gui.MessageDialog("No objects selected.")
            return
        ref_obj = selection[0]
        ref_mg = ref_obj.GetMg()
        ref_inv_mg = ~ref_mg
        mp = ref_obj.GetMp()
        rad = ref_obj.GetRad()
        p = ref_inv_mg * (ref_mg * (mp - rad))
        min_point = Vector(p)
        max_point = Vector(p + rad*2)
        for obj in selection:
            min_point, max_point = calculate_bounding_box_objects(obj, min_point, max_point, ref_inv_mg)
        primitive = create_bounding_primitive(primitive_type, axis, min_point, max_point, doc, ref_mg)

    elif mode in (c4d.Mpoints, c4d.Medges, c4d.Mpolygons):
        obj = doc.GetActiveObject()
        if not obj or not obj.IsInstanceOf(c4d.Opolygon):
            gui.MessageDialog("No valid polygon object selected.")
            return
        selected_points, _ = get_selected_points_from_selection(obj, mode)
        if not selected_points:
            gui.MessageDialog("No sub-object elements selected.")
            return
        ref_mg = obj.GetMg()
        ref_inv_mg = ~ref_mg
        points = obj.GetAllPoints()
        first_point = ref_inv_mg * (ref_mg * points[next(iter(selected_points))])
        min_point = Vector(first_point)
        max_point = Vector(first_point)
        for i in selected_points:
            p = ref_inv_mg * (ref_mg * points[i])
            min_point.x = min(min_point.x, p.x)
            min_point.y = min(min_point.y, p.y)
            min_point.z = min(min_point.z, p.z)
            max_point.x = max(max_point.x, p.x)
            max_point.y = max(max_point.y, p.y)
            max_point.z = max(max_point.z, p.z)
        primitive = create_bounding_primitive(primitive_type, axis, min_point, max_point, doc, ref_mg)
    else:
        gui.MessageDialog("Please switch to Object Mode or Sub-Object Mode.")
        return

    doc.EndUndo()
    doc.SetActiveObject(primitive, c4d.SELECTION_NEW)
    c4d.EventAdd()

if __name__ == '__main__':
    main()
