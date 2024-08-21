import c4d

def main():
    obj = doc.GetActiveObject()  # Obtén el objeto seleccionado
    if obj is None or not isinstance(obj, c4d.PolygonObject):
        return

    # Obtén los puntos actuales
    points = obj.GetAllPoints()
    point_count = obj.GetPointCount()

    # Aquí puedes definir tu nuevo orden de índices
    # Por ejemplo, intercambiar el primer y segundo punto
    new_order = list(range(point_count))
    new_order[0], new_order[15] = new_order[15], new_order[0]

    # Reordenar los puntos
    new_points = [points[i] for i in new_order]

    # Asignar los puntos reordenados al objeto
    obj.SetAllPoints(new_points)
    obj.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()

if __name__ == '__main__':
    main()