"""
Author: Mateo Vallejo
Website:
Version: 1.0.1
Description-US:Copy diplay color from parent to children of selected objects.
"""

import c4d

def apply_color_to_children(parent_obj, color_use, color_value):
    # Obtén los hijos del objeto actual
    children = parent_obj.GetChildren()
    
    # Recorre cada hijo
    for child in children:
        # Registra el estado del objeto antes de hacer los cambios
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)
        
        # Copia la propiedad de display color del padre al hijo
        child[c4d.ID_BASEOBJECT_USECOLOR] = color_use
        child[c4d.ID_BASEOBJECT_COLOR] = color_value
        child[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2  # Asegura que el color se muestre en el icono
        
        # Llama recursivamente a la función para procesar los descendientes
        apply_color_to_children(child, color_use, color_value)

def main():
    # Obtén los objetos seleccionados
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    # Verifica que haya al menos un objeto seleccionado
    if not selected:
        c4d.gui.MessageDialog("Por favor, selecciona al menos un objeto.")
        return

    # Comienza la operación de deshacer
    doc.StartUndo()

    # Recorre cada objeto seleccionado
    for parent_obj in selected:
        # Guarda las propiedades de color del objeto padre
        color_use = parent_obj[c4d.ID_BASEOBJECT_USECOLOR]
        color_value = parent_obj[c4d.ID_BASEOBJECT_COLOR]

        # Llama a la función para aplicar el color a todos los descendientes
        apply_color_to_children(parent_obj, color_use, color_value)

    # Termina la operación de deshacer
    doc.EndUndo()

    # Refresca el documento para ver los cambios
    c4d.EventAdd()

# Ejecuta la función principal
if __name__ == '__main__':
    main()
