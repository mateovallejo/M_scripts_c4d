"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Align selected vertices or objects on origin X.
"""

import c4d
from c4d import utils

def align_points(obj, doc):
    # Inicia una transacción para el historial de deshacer
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    mg = obj.GetMg()
    mg_inv = ~mg
    point_selection = obj.GetPointS()
    points = obj.GetAllPoints()
    for i, point in enumerate(points):
        if point_selection.IsSelected(i):
            global_point = point * mg
            global_point.x = 0
            local_point = global_point * mg_inv
            points[i] = local_point
    obj.SetAllPoints(points)
    obj.Message(c4d.MSG_UPDATE)
    doc.EndUndo()

def align_edges(obj, doc):
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    mg = obj.GetMg()
    mg_inv = ~mg
    edge_selection = obj.GetEdgeS()
    points = obj.GetAllPoints()
    poly_count = obj.GetPolygonCount()
    point_indices = set()
    # Loop through all polygons and their edges
    for poly_index in range(poly_count):
        poly = obj.GetPolygon(poly_index)
        # Handle triangles and quads
        is_quad = (poly.c != poly.d)
        edges = [ (poly.a, poly.b), (poly.b, poly.c) ]
        if is_quad:
            edges.append((poly.c, poly.d))
            edges.append((poly.d, poly.a))
        else:
            edges.append((poly.c, poly.a))
        for edge_id, (p1, p2) in enumerate(edges):
            eid = poly_index * 4 + edge_id  # Manual calculation of edge index
            if edge_selection.IsSelected(eid):
                point_indices.add(p1)
                point_indices.add(p2)
    for i in point_indices:
        global_point = points[i] * mg
        global_point.x = 0
        local_point = global_point * mg_inv
        points[i] = local_point
    obj.SetAllPoints(points)
    obj.Message(c4d.MSG_UPDATE)
    doc.EndUndo()

def align_polygons(obj, doc):
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    mg = obj.GetMg()
    mg_inv = ~mg
    poly_selection = obj.GetPolygonS()
    points = obj.GetAllPoints()
    poly_count = obj.GetPolygonCount()
    point_indices = set()
    for poly_index in range(poly_count):
        if poly_selection.IsSelected(poly_index):
            poly = obj.GetPolygon(poly_index)
            point_indices.update([poly.a, poly.b, poly.c, poly.d])
    for i in point_indices:
        global_point = points[i] * mg
        global_point.x = 0
        local_point = global_point * mg_inv
        points[i] = local_point
    obj.SetAllPoints(points)
    obj.Message(c4d.MSG_UPDATE)
    doc.EndUndo()

def align_objects(doc):
    # Inicia una transacción para el historial de deshacer
    doc.StartUndo()
    
    # Obtiene los objetos seleccionados
    selection = doc.GetSelection()
    
    for obj in selection:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        pos = obj.GetAbsPos()
        pos.x = 0
        obj.SetAbsPos(pos)
    
    doc.EndUndo()

def main():
    import c4d
    doc = c4d.documents.GetActiveDocument()
    mode = doc.GetMode()
    obj = doc.GetActiveObject()
    if obj and obj.IsInstanceOf(c4d.Opolygon):
        if mode == c4d.Mpoints:
            align_points(obj, doc)
        elif mode == c4d.Medges:
            align_edges(obj, doc)
        elif mode == c4d.Mpolygons:
            align_polygons(obj, doc)
        else:
            align_objects(doc)
    else:
        align_objects(doc)
    c4d.EventAdd()

if __name__ == '__main__':
    main()
