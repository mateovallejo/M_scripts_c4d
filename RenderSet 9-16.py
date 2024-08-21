import c4d

def main():
    # Obtén el documento actual
    doc = c4d.documents.GetActiveDocument()

    # Obtén la configuración de renderización
    render_data = doc.GetActiveRenderData()

    # Establece la resolución de salida
    render_data[c4d.RDATA_XRES] = 1920  # Ancho
    render_data[c4d.RDATA_YRES] = 1920  # Alto

    # Actualiza el documento
    c4d.EventAdd()

# Ejecuta la función principal
if __name__=='__main__':
    main()