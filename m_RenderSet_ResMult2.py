"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Multiply frame resolution by 2.
"""


import c4d

def main():
    # Obtener el documento actual
    doc = c4d.documents.GetActiveDocument()
    
    # Obtener las configuraciones de renderizado del documento actual
    render_data = doc.GetActiveRenderData()
    
    # Leer los valores actuales de la resolución
    x_res = render_data[c4d.RDATA_XRES]
    y_res = render_data[c4d.RDATA_YRES]
    
    # Dividir la resolución entre 2
    new_x_res = x_res * 2
    new_y_res = y_res * 2
    
    # Actualizar las configuraciones de renderizado con los nuevos valores
    render_data[c4d.RDATA_XRES] = new_x_res
    render_data[c4d.RDATA_YRES] = new_y_res
    
    # Actualizar el documento
    c4d.EventAdd()

# Ejecutar la función principal
if __name__=='__main__':
    main()
