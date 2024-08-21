import c4d


def main():
    # Obtén el documento actual
    doc = c4d.documents.GetActiveDocument()

    # Obtén la configuración de renderización
    render_data = doc.GetActiveRenderData()

    # Establece Current Frame
    render_data[c4d.RDATA_FRAMESEQUENCE] = 1
    
    # Actualiza el documento
    c4d.EventAdd()

# Ejecuta la función principal
if __name__=='__main__':
    main()