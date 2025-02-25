"""
Author: Mateo Vallejo (modificado)
Website:
Version: 1.3.3
Description-US: Create a Box object or an FFD deformer around selected objects or sub-object selection based on their bounding box.
             - In Object Mode, the bounding box is computed for all selected objects (including children).
             - In Sub-Object Mode (Points/Edges/Polygons), only the currently active selection is considered.
               The script forces a single selection type based on the active mode.
             - If the ALT key is pressed, an FFD deformer is created instead of a box.
"""

import c4d
from c4d import Vector

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

def calculate_bounding_box_sub(obj, selected_indices):
    """
    Compute the bounding box (global coordinates) for only the vertices whose indices
    are in the selected_indices set.
    """
    all_points = obj.GetAllPoints()
    mg = obj.GetMg()
    
    first_index = next(iter(selected_indices))
    first_point = mg * all_points[first_index]
    min_point = Vector(first_point.x, first_point.y, first_point.z)
    max_point = Vector(first_point.x, first_point.y, first_point.z)
    
    for i in selected_indices:
        p_global = mg * all_points[i]
        min_point.x = min(min_point.x, p_global.x)
        min_point.y = min(min_point.y, p_global.y)
        min_point.z = min(min_point.z, p_global.z)
        max_point.x = max(max_point.x, p_global.x)
        max_point.y = max(max_point.y, p_global.y)
        max_point.z = max(max_point.z, p_global.z)
    
    return min_point, max_point

def get_selected_points_from_selection(obj):
    """
    Returns a set of vertex indices based on the current sub-object selection.
    Checks in this order: vertices, edges, then faces.
    """
    points = set()
    
    # --- Vertex Selection ---
    point_sel = obj.GetPointS()
    if point_sel is not None and point_sel.GetCount() > 0:
        for i in range(obj.GetPointCount()):
            if point_sel.IsSelected(i):
                points.add(i)
        if points:
            return points, 'points'
    
    # --- Edge Selection ---
    edge_sel = obj.GetEdgeS()
    if edge_sel is not None and edge_sel.GetCount() > 0:
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
                if edge_sel.IsSelected(4 * i + j):
                    points.update(edge)
        if points:
            return points, 'edges'
    
    # --- Polygon (Face) Selection ---
    poly_sel = obj.GetPolygonS()
    if poly_sel is not None and poly_sel.GetCount() > 0:
        for i in range(obj.GetPolygonCount()):
            if poly_sel.IsSelected(i):
                poly = obj.GetPolygon(i)
                points.add(poly.a)
                points.add(poly.b)
                points.add(poly.c)
                if poly.d != poly.c:
                    points.add(poly.d)
        if points:
            return points, 'faces'
    
    return points, None

def main():
    doc = c4d.documents.GetActiveDocument()
    mode = doc.GetMode()  # Active selection mode
    doc.StartUndo()
    
    # --- Object Mode: Process all selected objects ---
    if mode == c4d.Mmodel:
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if not selection:
            c4d.gui.MessageDialog("No objects selected.")
            return
        
        # Initialize bounding box using the first selected object's first point.
        obj = selection[0]
        poly_obj = obj.GetCache()
        if poly_obj is None:
            poly_obj = obj
        points = poly_obj.GetAllPoints()
        if not points:
            c4d.gui.MessageDialog("The object has no points.")
            return
        mg = obj.GetMg()
        p = mg * points[0]
        min_point = Vector(p.x, p.y, p.z)
        max_point = Vector(p.x, p.y, p.z)
        
        for obj in selection:
            min_point, max_point = calculate_bounding_box_objects(obj, min_point, max_point)
    
    # --- Sub-Object Mode: Process only the selected vertices from the active object ---
    elif mode in (c4d.Mpoints, c4d.Medges, c4d.Mpolygons):
        obj = doc.GetActiveObject()
        if not obj or not obj.IsInstanceOf(c4d.Opolygon):
            c4d.gui.MessageDialog("No valid polygon object active.")
            return

        # Force only one type of sub-object selection based on the current mode.
        if mode == c4d.Mpoints:
            obj.GetEdgeS().DeselectAll()
            obj.GetPolygonS().DeselectAll()
        elif mode == c4d.Medges:
            obj.GetPointS().DeselectAll()
            obj.GetPolygonS().DeselectAll()
        elif mode == c4d.Mpolygons:
            obj.GetPointS().DeselectAll()
            obj.GetEdgeS().DeselectAll()
        
        selected_points, selection_type = get_selected_points_from_selection(obj)
        if not selected_points:
            c4d.gui.MessageDialog("No sub-object elements (vertices/edges/faces) selected.")
            return
        
        min_point, max_point = calculate_bounding_box_sub(obj, selected_points)
    
    else:
        c4d.gui.MessageDialog("Please switch to Object Mode or Sub-Object Mode (Points/Edges/Polygons).")
        return
    
    # Compute the bounding box size and center.
    size = max_point - min_point
    center = (max_point + min_point) / 2
    
    # --- Create object based on input state ---
    if isAltPressed():
        # Create an FFD deformer.
        new_obj = c4d.BaseObject(c4d.Offd)
        new_obj[c4d.FFDOBJECT_SIZE] = size
        new_obj.SetAbsPos(center)
        # Insert the FFD and call the reset BEFORE adding the undo.
        doc.InsertObject(new_obj)
        doc.AddUndo(c4d.UNDOTYPE_NEW, new_obj)
        c4d.CallButton(new_obj, c4d.FFDOBJECT_RESET)
        # Now add the undo for the FFD creation (including the reset state)
        doc.AddUndo(c4d.UNDOTYPE_NEW, new_obj)
    else:
        # Create a Cube.
        new_obj = c4d.BaseObject(c4d.Ocube)
        new_obj[c4d.PRIM_CUBE_LEN] = size
        new_obj.SetAbsPos(center)
        doc.InsertObject(new_obj)
        doc.AddUndo(c4d.UNDOTYPE_NEW, new_obj)
    
    doc.EndUndo()
    c4d.EventAdd()
    
    doc.SetActiveObject(new_obj, c4d.SELECTION_NEW)
    c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW | c4d.DRAWFLAGS_NO_THREAD | c4d.DRAWFLAGS_STATICBREAK)
    c4d.EventAdd()

if __name__ == '__main__':
    main()