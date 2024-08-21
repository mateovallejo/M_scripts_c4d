import c4d
from c4d import utils

def main():
    # Obtiene el objeto activo
    obj = doc.GetActiveObject()
    if obj is None or not obj.IsInstanceOf(c4d.Opolygon):
        return
    
    # Inicia una transacción para el historial de deshacer
    doc.StartUndo()
    
    # Añade un paso de deshacer para la selección de puntos
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    
    # Obtiene la matriz global del objeto
    mg = obj.GetMg()
    
    # Invierte la matriz global para convertir de global a local
    mg_inv = ~mg
    
    # Obtiene la selección de puntos
    point_selection = obj.GetPointS()
    points = obj.GetAllPoints()
    
    # Recorre todos los puntos
    for i, point in enumerate(points):
        # Verifica si el punto está seleccionado
        if point_selection.IsSelected(i):
            # Convierte la posición del punto a global
            global_point = point * mg
            
            # Establece la coordenada X a 0 en el espacio global
            global_point.z = 0
            
            # Convierte de nuevo a coordenadas locales
            local_point = global_point * mg_inv
            
            # Asigna la nueva posición al punto
            points[i] = local_point
    
    # Asigna las nuevas posiciones a los puntos del objeto
    obj.SetAllPoints(points)
    
    # Actualiza el objeto para reflejar los cambios
    obj.Message(c4d.MSG_UPDATE)
    
    # Finaliza la transacción de deshacer
    doc.EndUndo()
    
    # Marca el documento como sucio para indicar cambios
    c4d.EventAdd()

if __name__ == '__main__':
    main()
