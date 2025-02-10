import c4d

# Fallback: si c4d no tiene OmographCloner, se define
if not hasattr(c4d, "OmographCloner"):
    c4d.OmographCloner = 1018544

def gather_objects(root):
    """
    Recorre recursivamente la jerarquía a partir de 'root' y devuelve una lista de objetos.
    """
    objects = []
    while root:
        objects.append(root)
        if root.GetDown():
            objects += gather_objects(root.GetDown())
        root = root.GetNext()
    return objects

def rgb_to_vector(r, g, b):
    """
    Convierte valores RGB (0-255) a un c4d.Vector con valores en el rango 0-1.
    """
    return c4d.Vector(r / 255.0, g / 255.0, b / 255.0)

def main():
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo()

    # Determinar el rango de objetos a procesar:
    # Si hay objetos seleccionados, se usan estos y sus hijos; de lo contrario, se recorre toda la escena.
    selected_objs = doc.GetActiveObjects(0)
    if selected_objs:
        objects = []
        for obj in selected_objs:
            objects.extend(gather_objects(obj))
    else:
        firstObj = doc.GetFirstObject()
        if firstObj is None:
            doc.EndUndo()
            c4d.EventAdd()
            return
        objects = gather_objects(firstObj)

    # Filtra los cloners (MoGraph Cloner) de la lista de objetos a procesar
    cloners = [obj for obj in objects if obj.CheckType(c4d.OmographCloner)]
    
    for cloner in cloners:
        # Crea un null (grupo) con el mismo nombre que el cloner
        groupNull = c4d.BaseObject(c4d.Onull)
        groupNull.SetName(cloner.GetName())
        # Configura un icono y color para identificarlo (opcional)
        groupNull.SetParameter(c4d.ID_BASELIST_ICON_FILE, "1052838", c4d.DESCFLAGS_SET_0)
        groupNull[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2
        groupNull[c4d.ID_BASELIST_ICON_COLOR] = rgb_to_vector(108, 229, 130)  # Verde
        
        # Inserta el null en el documento y registra el undo
        doc.InsertObject(groupNull)
        doc.AddUndo(c4d.UNDOTYPE_NEW, groupNull)
        
        # Reubica el cloner: se remueve de su padre actual y se inserta bajo el null
        parent = cloner.GetUp()
        if parent:
            cloner.Remove()
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, parent)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, cloner)
        cloner.InsertUnder(groupNull)
        
        # Obtiene el objeto que contiene los effectors
        effectors = []
        effector_data = cloner[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
        if effector_data:
            count = effector_data.GetObjectCount()
            for i in range(count):
                # Se usa ObjectFromIndex para obtener cada effector
                eff = effector_data.ObjectFromIndex(doc, i)
                if eff:
                    effectors.append(eff)
        
        # Reubica cada effector para que quede como hijo del null
        for eff in effectors:
            parent_eff = eff.GetUp()
            if parent_eff:
                eff.Remove()
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, parent_eff)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, eff)
            eff.InsertUnder(groupNull)
        
        print("Agrupado el cloner '{}' con {} effector(es)".format(cloner.GetName(), len(effectors)))
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
