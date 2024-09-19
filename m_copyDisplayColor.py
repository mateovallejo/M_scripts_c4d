"""
Author: Mateo Vallejo
Website:
Version: 1.0.1
Description-US:Copy diplay color from first to second selected object.
"""

import c4d

def main():
    # Obtén todos los elementos seleccionados
    selection = doc.GetSelection()

    # Filtra solo los objetos (excluye etiquetas, materiales, etc.)
    selected = [s for s in selection if isinstance(s, c4d.BaseObject)]

    
    # Obtén el primer y segundo objeto seleccionado
    first_obj = selected[0]
    second_obj = selected[1]

    # Comienza la operación de deshacer
    doc.StartUndo()

    # Registra el estado del objeto antes de hacer los cambios
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, second_obj)

    # Copia la propiedad de color de visualización del primer objeto al segundo
    second_obj[c4d.ID_BASEOBJECT_USECOLOR] = first_obj[c4d.ID_BASEOBJECT_USECOLOR]
    second_obj[c4d.ID_BASEOBJECT_COLOR] = first_obj[c4d.ID_BASEOBJECT_COLOR]
    second_obj[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2

    # Termina la operación de deshacer
    doc.EndUndo()

    # Refresca el documento para ver los cambios
    c4d.EventAdd()

# Ejecuta la función principal
if __name__=='__main__':
    main()