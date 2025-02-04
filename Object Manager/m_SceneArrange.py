import c4d
import redshift as rs  # Asegúrate de que el módulo Redshift esté disponible

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

def get_or_create_null(doc, null_name):
    """
    Busca un objeto null con el nombre indicado. Si no lo encuentra, lo crea,
    lo inserta en el documento, asigna el icono especificado y registra su creación en el undo.
    """
    existing = doc.SearchObject(null_name)
    if existing:
        return existing

    new_null = c4d.BaseObject(c4d.Onull)
    new_null.SetName(null_name)
    
    # Inserta el objeto en el documento antes de asignar el icono
    doc.InsertObject(new_null)
    doc.AddUndo(c4d.UNDOTYPE_NEW, new_null)
    
    # Asigna el icono utilizando SetParameter(). Nota:
    # c4d.ID_BASELIST_ICON_FILE espera un string. En el script de ejemplo se usó "1052838"
    # (si fuese un icono interno puede ser necesario el prefijo '#' antes del ID).
    new_null.SetParameter(c4d.ID_BASELIST_ICON_FILE, "1052838", c4d.DESCFLAGS_SET_0)
    new_null.Message(c4d.MSG_UPDATE)  # Forzar la actualización del objeto
    
    return new_null

def GetTopParent(obj, groupNulls):
    """
    Sube por la jerarquía desde 'obj' hasta encontrar el ancestro más alto que no sea
    uno de los nulls de agrupación.
    """
    parent = obj.GetUp()
    while parent and (parent not in groupNulls):
        obj = parent
        parent = obj.GetUp()
    return obj

def branch_contains_cloner(obj):
    """
    Revisa la rama (el objeto y sus padres) para ver si alguno es un cloner.
    Devuelve True si se encuentra un cloner.
    """
    current = obj
    while current:
        if current.CheckType(c4d.OmographCloner):
            return True
        current = current.GetUp()
    return False

def main():
    doc = c4d.documents.GetActiveDocument()
    
    # Inicia un grupo de undo para toda la operación.
    doc.StartUndo()

    # Obtiene o crea los nulls de agrupación y registra su creación si son nuevos.
    lightsNull     = get_or_create_null(doc, "Lights")
    geoNull        = get_or_create_null(doc, "Geometry")
    camerasNull    = get_or_create_null(doc, "Cameras")
    generatorsNull = get_or_create_null(doc, "Generators")
    splinesNull    = get_or_create_null(doc, "Splines")  # Grupo para splines

    # Lista de nulls de agrupación para excluirlos al buscar el padre superior.
    groupNulls = [lightsNull, geoNull, camerasNull, generatorsNull, splinesNull]

    # Definimos los tipos de spline conocidos (incluye splines primitivas y convencionales).
    spline_types = [
        c4d.Ospline,
        c4d.Osplinerectangle,
        c4d.Osplinetext,
        c4d.Osplineprimitive,
        c4d.Osplinestar,
        c4d.Osplinearc,
        c4d.Osplinecircle,
        c4d.Osplinehelix,
        c4d.Osplinenside,
        c4d.Osplinecycloid,
        c4d.Ospline4side,
        c4d.Osplineflower,
        c4d.Osplinecogwheel
    ]

    # Recopila todos los objetos de la escena.
    topLevel = doc.GetFirstObject()
    allObjects = gather_objects(topLevel)

    # Para evitar mover la misma rama más de una vez.
    moved = set()

    for obj in allObjects:
        # Se ignoran los propios nulls de agrupación.
        if obj in groupNulls:
            continue

        group = None
        # Si en la rama se encuentra un cloner, se asigna al grupo "Generators".
        if branch_contains_cloner(obj):
            group = generatorsNull
        else:
            # Asignación según el tipo del objeto.
            if obj.CheckType(c4d.Ocamera) or obj.CheckType(c4d.Orscamera):
                group = camerasNull
            elif obj.CheckType(c4d.Olight) or obj.CheckType(c4d.Orslight):
                group = lightsNull
            # Comprueba si el objeto es de alguno de los tipos de spline.
            elif any(obj.CheckType(spline_type) for spline_type in spline_types):
                group = splinesNull
                # Mensaje de depuración:
                print("Spline detectado:", obj.GetName(), "Tipo:", obj.GetType())
            elif (obj.CheckType(c4d.Opolygon) or
                  obj.CheckType(c4d.Ocube) or
                  obj.CheckType(c4d.Osphere) or
                  obj.CheckType(c4d.Ocylinder) or
                  obj.CheckType(c4d.Ocone)):
                group = geoNull

        if group:
            # Obtiene el objeto raíz de la rama (excluyendo los nulls de agrupación).
            top = GetTopParent(obj, groupNulls)
            if id(top) in moved:
                continue

            # Guarda el padre original para que, al deshacer, se restaure la jerarquía.
            oldParent = top.GetUp()
            if oldParent:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, oldParent)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, top)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, group)

            # Mueve la rama: remueve el objeto y lo inserta bajo el grupo correspondiente.
            top.Remove()
            top.InsertUnder(group)

            moved.add(id(top))

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
