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
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, first_obj)

    # Copia las coordenadas del primer objeto al segundo
    first_obj.SetMg(second_obj.GetMg())

    # Registra el estado del objeto después de hacer los cambios
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, first_obj)

    # Termina la operación de deshacer
    doc.EndUndo()

    # Refresca el documento para ver los cambios
    c4d.EventAdd()

# Ejecuta la función principal
if __name__=='__main__':
    main()
