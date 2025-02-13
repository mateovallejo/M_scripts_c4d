"""
Author: Mateo Vallejo (modified by ChatGPT)
Version: 1.1.0
Description-US: Align selected elements (vertices, edges, or faces) so that in global space their X coordinate is 0.
"""

import c4d

def get_selected_points_from_selection(obj):
    """
    Returns a set of point indices based on the current selection.
    Checks in this order: vertices, edges, then faces.
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
            # Define the four edges of the polygon.
            # For triangles, polygon.d is usually equal to polygon.c.
            edges = [
                (poly.a, poly.b),
                (poly.b, poly.c),
                (poly.c, poly.d if poly.c != poly.d else poly.a),
                (poly.d, poly.a)
            ]
            # Each polygon has four potential edges; their selection indices are consecutive.
            for j, edge in enumerate(edges):
                if edge_sel.IsSelected(4 * i + j):
                    points.update(edge)
        return points, 'edges'
    
    # Face (polygon) selection
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
    obj = doc.GetActiveObject()
    # Make sure we have a polygon object
    if obj is None or not obj.IsInstanceOf(c4d.Opolygon):
        return

    # Optionally: Force only one type of selection active by deselecting others,
    # based on the current mode.
    mode = doc.GetMode()
    if mode == c4d.Mpoints:
        obj.GetEdgeS().DeselectAll()
        obj.GetPolygonS().DeselectAll()
    elif mode == c4d.Medges:
        obj.GetPointS().DeselectAll()
        obj.GetPolygonS().DeselectAll()
    elif mode == c4d.Mpolygons:
        obj.GetPointS().DeselectAll()
        obj.GetEdgeS().DeselectAll()
    else:
        c4d.gui.MessageDialog("No valid selection mode active. Please select points, edges, or polygons.")
        return

    # Get the set of vertex indices from the current selection.
    selected_points, sel_type = get_selected_points_from_selection(obj)
    if not selected_points:
        c4d.gui.MessageDialog("No vertices (from points, edges, or faces) are selected.")
        return

    # Start an undo transaction.
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    
    # Get the object's global matrix and its inverse.
    mg = obj.GetMg()
    mg_inv = ~mg

    # Get all points (in local space)
    points = obj.GetAllPoints()

    # For each selected vertex, convert its local position to global,
    # set the global X coordinate to 0, then convert back.
    for i in selected_points:
        global_point = points[i] * mg
        global_point.x = 0
        points[i] = global_point * mg_inv

    # Update the object's points.
    obj.SetAllPoints(points)
    obj.Message(c4d.MSG_UPDATE)
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
