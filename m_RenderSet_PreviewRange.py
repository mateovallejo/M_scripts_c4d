"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Set frame range to "Preview Range".
"""


import c4d


def main():
    # Obtén el documento actual
    doc = c4d.documents.GetActiveDocument()

    # Obtén la configuración de renderización
    render_data = doc.GetActiveRenderData()

    # Establece PreviewRange
    render_data[c4d.RDATA_FRAMESEQUENCE] = 3
    
    # Actualiza el documento
    c4d.EventAdd()

# Ejecuta la función principal
if __name__=='__main__':
    main()