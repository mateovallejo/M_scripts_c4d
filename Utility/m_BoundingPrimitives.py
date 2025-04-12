"""
Author: Mateo Vallejo
Version: 1.1.0
Description: Creates a primitive that matches the bounding box dimensions of selected objects.
- Choose from Box, Sphere, Cylinder, Cone, Pyramid, Tube, or Capsule
- Works in both Object Mode and Sub-Object Mode
- In Object Mode, considers all selected objects and their children
- In Sub-Object Mode, considers only the active selection
"""

import c4d
from c4d import gui, Vector

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

def calculate_bounding_box_objects(obj, min_point, max_point):
    """
    Recursively compute the bounding box of an object and its children (in global coordinates).
    """
    poly_obj = obj.GetCache()
    if poly_obj is None:
        poly_obj = obj

    points = poly_obj.GetAllPoints()
    mg = obj.GetMg()

    for p in points:
        p_global = mg * p
        min_point = Vector(min(min_point.x, p_global.x),
                           min(min_point.y, p_global.y),
                           min(min_point.z, p_global.z))
        max_point = Vector(max(max_point.x, p_global.x),
                           max(max_point.y, p_global.y),
                           max(max_point.z, p_global.z))
    
    child = obj.GetDown()
    while child:
        min_point, max_point = calculate_bounding_box_objects(child, min_point, max_point)
        child = child.GetNext()
    
    return min_point, max_point

def get_selected_points_from_selection(obj):
    """
    Returns a set of vertex indices based on the current sub-object selection.
    """
    points = set()
    
    # Vertex selection
    point_sel = obj.GetPointS()
    if point_sel.GetCount() > 0:
        for i in range(obj.GetPointCount()):
            if point_sel.IsSelected(i):
                points.add(i)
        return points, 'points'
    
    # Edge selection
    edge_sel = obj.GetEdgeS()
    if edge_sel.GetCount() > 0:
        polygons = obj.GetAllPolygons()
        for i in range(obj.GetPolygonCount()):
            poly = polygons[i]
            edges = [
                (poly.a, poly.b),
                (poly.b, poly.c),
                (poly.c, poly.d if poly.c != poly.d else poly.a),
                (poly.d, poly.a)
            ]
            for j, edge in enumerate(edges):
                if edge_sel.IsSelected(4*i + j):
                    points.update(edge)
        return points, 'edges'

    # Face selection
    poly_sel = obj.GetPolygonS()
    if poly_sel.GetCount() > 0:
        for i in range(obj.GetPolygonCount()):
            if poly_sel.IsSelected(i):
                poly = obj.GetPolygon(i)
                points.update([poly.a, poly.b, poly.c, poly.d])
        return points, 'faces'
    
    return points, None

def create_dropdown_menu():
    """
    Creates and shows a dropdown menu for primitive selection.
    """
    menu_entries = {
        c4d.Ocube: "Box",
        c4d.Osphere: "Sphere",
        c4d.Ocylinder: "Cylinder",
        c4d.Ocone: "Cone",
        c4d.Opyramid: "Pyramid",
        c4d.Otube: "Tube",
        c4d.Ocapsule: "Capsule"
    }
    
    entries = c4d.BaseContainer()
    for primitive_id, label in menu_entries.items():
        entries.SetString(primitive_id, label)
    
    return gui.ShowPopupDialog(
        cd=None,
        bc=entries,
        x=c4d.MOUSEPOS,
        y=c4d.MOUSEPOS,
        flags=c4d.POPUP_RIGHT
    )

def create_bounding_primitive(primitive_type, min_point, max_point, doc):
    """
    Creates a primitive that matches the bounding box dimensions.
    """
    size = max_point - min_point
    center = (max_point + min_point) / 2
    
    primitive = c4d.BaseObject(primitive_type)
    
    # Set dimensions based on primitive type
    if primitive_type == c4d.Ocube:
        primitive[c4d.PRIM_CUBE_LEN] = size
    
    elif primitive_type == c4d.Osphere:
        radius = max(size.x, size.y, size.z) / 2
        primitive[c4d.PRIM_SPHERE_RAD] = radius
    
    elif primitive_type == c4d.Ocylinder:
        radius = max(size.x, size.z) / 2
        primitive[c4d.PRIM_CYLINDER_RADIUS] = radius
        primitive[c4d.PRIM_CYLINDER_HEIGHT] = size.y
    
    elif primitive_type == c4d.Ocone:
        radius = max(size.x, size.z) / 2
        primitive[c4d.PRIM_CONE_TRAD] = 0
        primitive[c4d.PRIM_CONE_BRAD] = radius
        primitive[c4d.PRIM_CONE_HEIGHT] = size.y
    
    elif primitive_type == c4d.Opyramid:
        primitive[c4d.PRIM_PYRAMID_LEN] = size  # Fixed: Using correct parameter for pyramid
    
    elif primitive_type == c4d.Otube:
        radius = max(size.x, size.z) / 2
        primitive[c4d.PRIM_TUBE_ORAD] = radius
        primitive[c4d.PRIM_TUBE_IRAD] = radius * 0.8
        primitive[c4d.PRIM_TUBE_HEIGHT] = size.y
    
    elif primitive_type == c4d.Ocapsule:
        radius = max(size.x, size.z) / 2
        primitive[c4d.PRIM_CAPSULE_RADIUS] = radius
        primitive[c4d.PRIM_CAPSULE_HEIGHT] = size.y
    
    primitive.SetAbsPos(center)
    doc.InsertObject(primitive)
    doc.AddUndo(c4d.UNDOTYPE_NEW, primitive)
    
    return primitive

def main():
    # Show primitive selection dialog
    primitive_type = create_dropdown_menu()
    if not primitive_type:
        return
        
    doc = c4d.documents.GetActiveDocument()
    mode = doc.GetMode()
    doc.StartUndo()
    
    if mode == c4d.Mmodel:
        # Object mode - get all selected objects
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if not selection:
            c4d.gui.MessageDialog("No objects selected.")
            return
        
        # Initialize bounding box with first point
        obj = selection[0]
        points = obj.GetAllPoints()
        if not points:
            c4d.gui.MessageDialog("Selected object has no points.")
            return
        
        p = obj.GetMg() * points[0]
        min_point = Vector(p)
        max_point = Vector(p)
        
        # Calculate bounds for all selected objects
        for obj in selection:
            min_point, max_point = calculate_bounding_box_objects(obj, min_point, max_point)
    
    elif mode in (c4d.Mpoints, c4d.Medges, c4d.Mpolygons):
        # Sub-object mode - handle active selection
        obj = doc.GetActiveObject()
        if not obj or not obj.IsInstanceOf(c4d.Opolygon):
            c4d.gui.MessageDialog("No valid polygon object selected.")
            return
        
        selected_points, _ = get_selected_points_from_selection(obj)
        if not selected_points:
            c4d.gui.MessageDialog("No sub-object elements selected.")
            return
        
        # Calculate bounds for selected points
        points = obj.GetAllPoints()
        mg = obj.GetMg()
        first_point = mg * points[next(iter(selected_points))]
        min_point = Vector(first_point)
        max_point = Vector(first_point)
        
        for i in selected_points:
            p = mg * points[i]
            min_point.x = min(min_point.x, p.x)
            min_point.y = min(min_point.y, p.y)
            min_point.z = min(min_point.z, p.z)
            max_point.x = max(max_point.x, p.x)
            max_point.y = max(max_point.y, p.y)
            max_point.z = max(max_point.z, p.z)
    
    else:
        c4d.gui.MessageDialog("Please switch to Object Mode or Sub-Object Mode.")
        return
    
    # Create the selected primitive
    primitive = create_bounding_primitive(primitive_type, min_point, max_point, doc)
    
    doc.EndUndo()
    doc.SetActiveObject(primitive, c4d.SELECTION_NEW)
    c4d.EventAdd()

if __name__ == '__main__':
    main()
