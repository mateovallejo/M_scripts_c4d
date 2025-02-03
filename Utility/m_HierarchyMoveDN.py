import c4d

def main():
    doc.StartUndo()  # Iniciar registro de deshacer

    # Obtener objetos seleccionados
    seleccion = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)


    # Procesar los objetos en orden inverso para mantener el orden correcto al mover hacia abajo
    for obj in reversed(seleccion):
        siguiente = obj.GetNext()  # Obtener el objeto siguiente en la lista
        if siguiente is not None:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            # Eliminar el objeto de su posición actual
            obj.Remove()
            # Insertar el objeto después del siguiente
            obj.InsertAfter(siguiente)

    doc.EndUndo()  # Finalizar registro de deshacer
    c4d.EventAdd()  # Actualizar la escena

if __name__=='__main__':
    main()
