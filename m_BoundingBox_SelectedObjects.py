"""
Author: Mateo Vallejo (modificado)
Website:
Version: 1.0.0
Description-US: Create a Box object around selected objects based on their bounding box.
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

    # Iterar sobre los hijos del objeto
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

    # Iterar sobre cada objeto en la selección para calcular el bounding box total
    for obj in selection:
        min_point, max_point = calculate_bounding_box(obj, min_point, max_point)

    # Comenzar la operación de deshacer
    doc.StartUndo()

    # Crear un nuevo objeto cubo
    cube = c4d.BaseObject(c4d.Ocube)

    # Establecer el tamaño del cubo para que coincida con el bounding box
    size = max_point - min_point
    cube[c4d.PRIM_CUBE_LEN] = size

    # Establecer la posición del cubo al centro del bounding box
    cube.SetAbsPos((max_point + min_point) / 2)

    # Añadir el cubo a la escena
    doc.InsertObject(cube)
    doc.AddUndo(c4d.UNDOTYPE_NEW, cube)

    # Finalizar la operación de deshacer
    doc.EndUndo()

    # Actualizar la escena
    c4d.EventAdd()

    # Seleccionar el cubo generado
    doc.SetActiveObject(cube, c4d.SELECTION_NEW)
    c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW | c4d.DRAWFLAGS_NO_THREAD | c4d.DRAWFLAGS_STATICBREAK)

    c4d.EventAdd()

# Ejecutar el script
if __name__ == '__main__':
    main()
