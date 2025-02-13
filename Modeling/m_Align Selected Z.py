"""
Author: Mateo Vallejo (modified by ChatGPT)
Website:
Version: 1.1.0
Description-US: Align selected elements on Z.
Additional functionality:
  - When Alt is pressed, align to maximum Z value.
  - When Ctrl is pressed, align to minimum Z value.
  - Works in both object (model) mode and sub-object mode.
"""

import c4d

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

def get_selected_points_from_selection(obj):
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
            polygon = polygons[i]
            edges = [
                (polygon.a, polygon.b), 
                (polygon.b, polygon.c), 
                (polygon.c, polygon.d if polygon.c != polygon.d else polygon.a), 
                (polygon.d, polygon.a)
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
                points.add(poly.a)
                points.add(poly.b)
                points.add(poly.c)
                if poly.d != poly.c:
                    points.add(poly.d)
        return points, 'faces'
    
    return points, None

def main():
    doc = c4d.documents.GetActiveDocument()
    mode = doc.GetMode()  # Active selection mode
    
    # --- Object Mode (Model Mode) Alignment ---
    # In object mode (typically c4d.Mmodel), align object positions.
    if mode == c4d.Mmodel:
        objs = doc.GetActiveObjects(0)
        if not objs:
            return "No objects selected."
            
        doc.StartUndo()
        for obj in objs:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        
        # Gather all Z positions from the objects (using absolute/global positions)
        z_values = [obj.GetAbsPos().z for obj in objs]
        
        # Determine alignment value based on modifier keys
        if isAltPressed():
            align_value = max(z_values)
        elif isCtrlPressed():
            align_value = min(z_values)
        else:
            align_value = sum(z_values) / len(z_values)
        
        # Align each object to the computed Z value
        for obj in objs:
            pos = obj.GetAbsPos()
            pos.z = align_value
            obj.SetAbsPos(pos)
            obj.Message(c4d.MSG_UPDATE)
        
        doc.EndUndo()
        c4d.EventAdd()
        return

    # --- Sub-Object Mode Alignment ---
    # If not in object mode, then we expect a sub-object selection (points, edges, or polygons).
    if mode not in (c4d.Mpoints, c4d.Medges, c4d.Mpolygons):
        return "No valid selection mode active. Please select points, edges, polygons or switch to object mode."
    
    obj = doc.GetActiveObject()
    if not obj:
        return "No active object."
    
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    
    # Deselect non-relevant selection types
    if mode == c4d.Mpoints:
        edge_sel = obj.GetEdgeS()
        edge_sel.DeselectAll()
        poly_sel = obj.GetPolygonS()
        poly_sel.DeselectAll()
    elif mode == c4d.Medges:
        point_sel = obj.GetPointS()
        point_sel.DeselectAll()
        poly_sel = obj.GetPolygonS()
        poly_sel.DeselectAll()
    elif mode == c4d.Mpolygons:
        point_sel = obj.GetPointS()
        point_sel.DeselectAll()
        edge_sel = obj.GetEdgeS()
        edge_sel.DeselectAll()
    
    selected_points, selection_type = get_selected_points_from_selection(obj)
    if not selected_points:
        return "No vertices/edges/faces selected."
    
    all_points = obj.GetAllPoints()
    z_values = [all_points[i].z for i in selected_points]
    
    # Determine the alignment value based on modifier keys
    if isAltPressed():
        align_value = max(z_values)
    elif isCtrlPressed():
        align_value = min(z_values)
    else:
        align_value = sum(z_values) / len(z_values)
    
    # Align selected points to the computed Z value
    for i in selected_points:
        all_points[i].z = align_value
    
    obj.SetAllPoints(all_points)
    obj.Message(c4d.MSG_UPDATE)
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
