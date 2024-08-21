import c4d
from c4d import gui

def main():
    # Obtenemos la lista de objetos seleccionados
    seleccion = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    # Si no hay objetos seleccionados, terminamos
    if not seleccion:
        gui.MessageDialog("Por favor selecciona al menos un objeto.")
        return

    # Deseleccionamos todos los objetos
    doc.SetActiveObject(None, c4d.SELECTION_NEW)

    # Para cada objeto en la selección
    for obj in seleccion:
        # Seleccionamos el primer hijo
        hijo = obj.GetDown()
        if hijo:
            doc.SetActiveObject(hijo, c4d.SELECTION_ADD)

    # Actualizamos la interfaz
    c4d.EventAdd()

# Ejecutamos la función main
if __name__=='__main__':
    main()
