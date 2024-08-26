"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Copy diplay color from first to second selected object.
"""

import c4d

def main():
    # Obtén los objetos seleccionados
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    # Verifica que haya al menos dos objetos seleccionados
    if len(selected) < 2:
        print("Por favor selecciona al menos dos objetos")
        return

    # Obtén el primer y segundo objeto seleccionado
    first_obj = selected[0]
    second_obj = selected[1]

    # Comienza la operación de deshacer
    doc.StartUndo()

    # Registra el estado del objeto antes de hacer los cambios
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, second_obj)  # Cambiado a second_obj porque es donde se aplicará el cambio

    # Copia la propiedad de display color del primer objeto al segundo
    second_obj[c4d.ID_BASEOBJECT_USECOLOR] = first_obj[c4d.ID_BASEOBJECT_USECOLOR]
    second_obj[c4d.ID_BASEOBJECT_COLOR] = first_obj[c4d.ID_BASEOBJECT_COLOR]
    second_obj[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2

    # Registra el estado del objeto después de hacer los cambios
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, second_obj)

    # Termina la operación de deshacer
    doc.EndUndo()

    # Refresca el documento para ver los cambios
    c4d.EventAdd()

# Ejecuta la función principal
if __name__=='__main__':
    main()