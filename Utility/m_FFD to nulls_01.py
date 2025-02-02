import c4d

def main():
    doc.StartUndo()
    
    # Obtiene el objeto seleccionado
    obj = doc.GetActiveObject()
    if obj is None:
        c4d.gui.MessageDialog("No hay ningún objeto seleccionado.")
        return
    
    # Verifica que el objeto sea un FFD
    if obj.GetType() != c4d.Offd:
        c4d.gui.MessageDialog("Por favor, selecciona un objeto FFD.")
        return
    
    # Obtiene todos los puntos (vértices) del FFD
    points = obj.GetAllPoints()
    if not points:
        c4d.gui.MessageDialog("No se han encontrado puntos en el objeto FFD seleccionado.")
        return
    
    # Obtiene la matriz global del FFD para calcular posiciones globales
    mg = obj.GetMg()
    
    # Crea un Null por cada vértice
    for i, p in enumerate(points):
        nullObj = c4d.BaseObject(c4d.Onull)
        nullObj.SetName("Vertex_{}".format(i))
        
        # Calcula la posición global del punto
        globalPos = mg * p
        # Ajusta la matriz del Null para que su posición sea la del vértice
        nullObj.SetMg(c4d.Matrix(off=globalPos))
        
        doc.InsertObject(nullObj)
        doc.AddUndo(c4d.UNDOTYPE_NEW, nullObj)
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
