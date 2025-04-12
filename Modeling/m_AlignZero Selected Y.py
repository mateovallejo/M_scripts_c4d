"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Align selected vertices or objects on origin Y.
"""

import c4d
from c4d import utils

def align_points(obj, doc):
    # Inicia una transacción para el historial de deshacer
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    
    # Obtiene la matriz global del objeto
    mg = obj.GetMg()
    mg_inv = ~mg
    
    # Obtiene la selección de puntos
    point_selection = obj.GetPointS()
    points = obj.GetAllPoints()
    
    # Recorre todos los puntos
    for i, point in enumerate(points):
        if point_selection.IsSelected(i):
            global_point = point * mg
            global_point.y = 0
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
        pos.y = 0
        obj.SetAbsPos(pos)
    
    doc.EndUndo()

def main():
    # Check current mode
    mode = doc.GetMode()
    
    if mode == c4d.Mpoints:  # Point mode
        obj = doc.GetActiveObject()
        if obj and obj.IsInstanceOf(c4d.Opolygon):
            align_points(obj, doc)
    else:  # Object mode
        align_objects(doc)
    
    # Actualiza la vista
    c4d.EventAdd()

if __name__ == '__main__':
    main()
