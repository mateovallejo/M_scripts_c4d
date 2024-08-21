"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Align selected vertices on X.
"""

import c4d

def get_selected_points_from_selection(obj):
    points = set()
    
    # Selección de vértices
    point_sel = obj.GetPointS()
    if point_sel.GetCount() > 0:
        for i in range(obj.GetPointCount()):
            if point_sel.IsSelected(i):
                points.add(i)
        return points, 'points'
    
    # Selección de aristas
    edge_sel = obj.GetEdgeS()
    if edge_sel.GetCount() > 0:
        polygons = obj.GetAllPolygons()
        for i in range(obj.GetPolygonCount()):
            polygon = polygons[i]
            edges = [(polygon.a, polygon.b), 
                     (polygon.b, polygon.c), 
                     (polygon.c, polygon.d if polygon.c != polygon.d else polygon.a), 
                     (polygon.d, polygon.a)]
            for j, edge in enumerate(edges):
                if edge_sel.IsSelected(4*i + j):
                    points.update(edge)
        return points, 'edges'

    # Selección de caras
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
    if not obj:
        return

    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

    # Obtener el tipo de selección activo
    mode = doc.GetMode()
    
    # Deseleccionar según el tipo de selección activo
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
        
    else:
        return "No hay una selección de vértices, aristas o caras activa."

    selected_points, selection_type = get_selected_points_from_selection(obj)
    
    all_points = obj.GetAllPoints()
    x_values = [all_points[i].x for i in selected_points]
    avg_x = sum(x_values) / len(x_values)

    for i in selected_points:
        all_points[i].x = avg_x

    obj.SetAllPoints(all_points)
    obj.Message(c4d.MSG_UPDATE)
    
    doc.EndUndo()
    c4d.EventAdd()

    
if __name__=='__main__':
    main()
