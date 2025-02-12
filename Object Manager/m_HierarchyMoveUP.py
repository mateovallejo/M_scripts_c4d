"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Moves each selected object up one position in the hierarchy.
"""
import c4d

def main():
    doc.StartUndo()  # Iniciar registro de deshacer

    # Obtener objetos seleccionados
    seleccion = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

    if not seleccion:
        c4d.gui.MessageDialog('No hay objetos seleccionados.')
        return

    for obj in seleccion:
        anterior = obj.GetPred()  # Obtener el objeto anterior en la lista
        if anterior is not None:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            # Eliminar el objeto de su posición actual
            obj.Remove()
            # Insertar el objeto antes del anterior
            obj.InsertBefore(anterior)

    doc.EndUndo()  # Finalizar registro de deshacer
    c4d.EventAdd()  # Actualizar la escena

if __name__=='__main__':
    main()
