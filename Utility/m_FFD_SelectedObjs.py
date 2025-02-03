"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Add FFD object to selected objects.
"""

import c4d
from c4d import Vector, BaseObject, utils

def calculate_bounding_box(obj, min_point, max_point):
    # Convertir el objeto a poligonal si es necesario
    poly_obj = obj.GetCache()
    if poly_obj is None:
        poly_obj = obj

    # Obtener los puntos del objeto
    points = poly_obj.GetAllPoints()
    mg = obj.GetMg()  # Matriz global del objeto

    # Iterar sobre cada punto
    for p in points:
        # Convertir a coordenadas globales
        p_global = mg * p

        # Actualizar los límites si es necesario
        min_point = Vector(min(min_point.x, p_global.x), min(min_point.y, p_global.y), min(min_point.z, p_global.z))
        max_point = Vector(max(max_point.x, p_global.x), max(max_point.y, p_global.y), max(max_point.z, p_global.z))

    # Iterar sobre cada hijo del objeto
    child = obj.GetDown()
    while child:
        min_point, max_point = calculate_bounding_box(child, min_point, max_point)
        child = child.GetNext()

    return min_point, max_point

def main():
    # Obtener la selección de objetos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    if not selection:
        return

    # Establecer los límites iniciales en base al primer objeto seleccionado
    obj = selection[0].GetCache()
    if obj is None:
        obj = selection[0]
    points = obj.GetAllPoints()
    p = obj.GetMg() * points[0]  # Transformación a coordenadas globales
    min_point = p
    max_point = p

    # Iterar sobre cada objeto en la selección
    for obj in selection:
        min_point, max_point = calculate_bounding_box(obj, min_point, max_point)

    # Comenzar la operación de deshacer
    doc.StartUndo()

    # Crear un nuevo deformer FFD
    ffd = c4d.BaseObject(c4d.Offd)

    # Establecer el tamaño del FFD para que coincida con el bounding box
    ffd[c4d.FFDOBJECT_SIZE] = max_point - min_point

    # Establecer la posición del FFD al centro del bounding box
    ffd.SetAbsPos((max_point + min_point) / 2)

    # Añadir el FFD a la escena
    doc.InsertObject(ffd)

    # Registrar la operación de deshacer
    doc.AddUndo(c4d.UNDOTYPE_NEW, ffd)

    # Finalizar la operación de deshacer
    doc.EndUndo()

    # Actualizar la escena
    c4d.EventAdd()

    # Seleccionar el objeto FFD generado
    doc.SetActiveObject(ffd)  # Establecer el FFD como objeto activo
    c4d.CallCommand(12236)  # Comando para seleccionar el objeto activo (Select All)

    # Actualizar la vista para reflejar la selección
    c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW | c4d.DRAWFLAGS_NO_THREAD | c4d.DRAWFLAGS_STATICBREAK)

    c4d.EventAdd()
    c4d.CallButton(ffd, c4d.FFDOBJECT_RESET)

# Ejecutar el script
if __name__ == '__main__':
    main()
