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

def get_or_create_null(doc, null_name, display_color):
    """
    Busca un objeto null con el nombre indicado. Si no lo encuentra, lo crea,
    lo inserta en el documento, asigna el icono especificado, configura el display color 
    y el icon colorize mode, y registra su creación en el undo.
    """
    existing = doc.SearchObject(null_name)
    if existing:
        # Si ya existe, se actualizan los parámetros deseados.
        existing.SetParameter(c4d.ID_BASELIST_ICON_FILE, "1052838", c4d.DESCFLAGS_SET_0)
        existing[c4d.ID_BASELIST_ICON_COLOR] = display_color
        return existing

    new_null = c4d.BaseObject(c4d.Onull)
    new_null.SetName(null_name)
    
    # Inserta el objeto en el documento y registra el undo.
    doc.InsertObject(new_null)
    doc.AddUndo(c4d.UNDOTYPE_NEW, new_null)
    
    # Asigna el icono y configura el display color y el icon colorize mode.
    new_null.SetParameter(c4d.ID_BASELIST_ICON_FILE, "1052838", c4d.DESCFLAGS_SET_0)
    new_null[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2
    new_null[c4d.ID_BASELIST_ICON_COLOR] = display_color
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

def rgb_to_vector(r, g, b):
    """
    Convierte valores RGB (0-255) a un c4d.Vector con valores en el rango 0-1.
    """
    return c4d.Vector(r / 255.0, g / 255.0, b / 255.0)

def main():
    doc = c4d.documents.GetActiveDocument()
    
    # Inicia un grupo de undo para toda la operación.
    doc.StartUndo()

    # Obtiene o crea los nulls de agrupación, asignándoles un color de display (en formato RGB).
    lightsNull     = get_or_create_null(doc, "Lights",     rgb_to_vector(255, 255, 0))   # Amarillo
    geoNull        = get_or_create_null(doc, "Geometry",   rgb_to_vector(70, 250, 200)) # Turquesa
    camerasNull    = get_or_create_null(doc, "Cameras",    rgb_to_vector(255, 60, 80))     # Rojo
    generatorsNull = get_or_create_null(doc, "Generators", rgb_to_vector(108, 229, 130))   # Verde Claro
    splinesNull    = get_or_create_null(doc, "Splines",    rgb_to_vector(140, 220, 250))     # Celeste

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
    
    # Definimos los tipos de primitivos.
    primitive_types = [
        c4d.Ocube,
        c4d.Osphere,
        c4d.Ocylinder,
        c4d.Ocone,
        c4d.Oplane,
        c4d.Opyramid,
        c4d.Otorus,
        c4d.Otube,
        c4d.Ocapsule,
        c4d.Ofractal,
        c4d.Odisc,
        c4d.Oplatonic,
        c4d.Ofigure,
        c4d.Opolygon  # Se incluye Opolygon en caso de que se considere primitivo en el contexto
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
            # Comprueba si el objeto es de alguno de los tipos de primitivos.
            elif any(obj.CheckType(primitive_type) for primitive_type in primitive_types):
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
