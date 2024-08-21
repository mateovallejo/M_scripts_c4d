import c4d

def main():
    # Obtén el documento actual
    doc = c4d.documents.GetActiveDocument()

    # Obtén la configuración de renderización
    render_data = doc.GetActiveRenderData()

    # Lee el estado actual del parámetro RDATA_SAVEIMAGE
    current_state = render_data[c4d.RDATA_SAVEIMAGE]

    # Cambia el estado del parámetro RDATA_SAVEIMAGE usando una declaración if
    if current_state == True:
        render_data[c4d.RDATA_SAVEIMAGE] = False
        c4d.gui.MessageDialog('Save OFF')
    elif current_state == False:
        render_data[c4d.RDATA_SAVEIMAGE] = True
        c4d.gui.MessageDialog('Save ON')

    # Actualiza el documento
    c4d.EventAdd()

# Ejecuta la función principal
if __name__=='__main__':
    main()
