"""
Author: Mateo Vallejo / Modified by [Your Name]
Version: 1.6.0
Description-US: Groups each selected cloner and its effectors under a new null. CTRL: Also group linked objects.
"""
import c4d

# Fallback: if c4d does not have OmographCloner, define it.
if not hasattr(c4d, "OmographCloner"):
    c4d.OmographCloner = 1018544

def gather_objects(root):
    """
    Recursively traverse the hierarchy from 'root' and return a list of objects.
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
    Convert RGB values (0-255) to a c4d.Vector with values in the range 0-1.
    """
    return c4d.Vector(r / 255.0, g / 255.0, b / 255.0)

def isCtrlPressed():
    """
    Returns True if the CTRL key is pressed.
    """
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        if qualifier & c4d.QCTRL:
            return True
    return False

def group_fields(effector, doc):
    """
    If the effector has fields, group all field objects that are not already children of the effector
    under a new null.
    """
    field_list = effector.GetParameter(c4d.DescID(c4d.FIELDS), c4d.DESCFLAGS_GET_NONE)
    if not field_list or field_list.GetCount() == 0:
        return

    field_objects = []
    layers_root = field_list.GetLayersRoot()
    if layers_root:
        layer = layers_root.GetFirst()
        while layer:
            linked_obj = layer.GetLinkedObject(doc)
            if linked_obj:
                field_objects.append(linked_obj)
            layer = layer.GetNext()

    field_objects_to_move = [obj for obj in field_objects if obj.GetUp() != effector]
    if not field_objects_to_move:
        return

    fieldsNull = c4d.BaseObject(c4d.Onull)
    fieldsNull.SetName(effector.GetName() + " Fields")
    parent = effector.GetUp()
    doc.AddUndo(c4d.UNDOTYPE_NEW, fieldsNull)
    doc.InsertObject(fieldsNull, parent=parent, pred=effector)

    for field_obj in field_objects_to_move:
        parent_field = field_obj.GetUp()
        if parent_field:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, parent_field)
            field_obj.Remove()
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, field_obj)
        field_obj.InsertUnderLast(fieldsNull)

def main():
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo()

    cloners = []
    selected_objs = doc.GetActiveObjects(0)
    if selected_objs:
        selected_cloners = [obj for obj in selected_objs if obj.CheckType(c4d.OmographCloner)]
        if selected_cloners:
            cloners = selected_cloners
        else:
            objects = []
            for obj in selected_objs:
                objects.extend(gather_objects(obj))
            cloners = [obj for obj in objects if obj.CheckType(c4d.OmographCloner)]
    else:
        firstObj = doc.GetFirstObject()
        if firstObj:
            objects = gather_objects(firstObj)
            cloners = [obj for obj in objects if obj.CheckType(c4d.OmographCloner)]

    for cloner in cloners:
        groupNull = c4d.BaseObject(c4d.Onull)
        groupNull.SetName(cloner.GetName())
        groupNull.SetParameter(c4d.ID_BASELIST_ICON_FILE, "1052838", c4d.DESCFLAGS_SET_0)
        groupNull[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2

        # Transfer the cloner's display color to the null's icon color.
        cloner_color = cloner[c4d.ID_BASEOBJECT_COLOR]
        groupNull[c4d.ID_BASELIST_ICON_COLOR] = cloner_color

        parent = cloner.GetUp()
        doc.AddUndo(c4d.UNDOTYPE_NEW, groupNull)
        if parent:
            doc.InsertObject(groupNull, parent=parent, pred=cloner)
        else:
            doc.InsertObject(groupNull)

        if parent:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, parent)
            cloner.Remove()
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, cloner)
        cloner.InsertUnder(groupNull)

        effectors = []
        effector_data = cloner[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
        if effector_data:
            count = effector_data.GetObjectCount()
            for i in range(count):
                eff = effector_data.ObjectFromIndex(doc, i)
                if eff:
                    effectors.append(eff)

        for eff in effectors:
            parent_eff = eff.GetUp()
            if parent_eff:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, parent_eff)
                eff.Remove()
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, eff)
            eff.InsertUnder(groupNull)
            group_fields(eff, doc)

        # If CTRL is pressed, also consider the linked object from the cloner.
        if isCtrlPressed():
            linked_obj = cloner[c4d.MG_OBJECT_LINK]
            if linked_obj:
                parent_link = linked_obj.GetUp()
                if parent_link:
                    doc.AddUndo(c4d.UNDOTYPE_CHANGE, parent_link)
                    linked_obj.Remove()
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, linked_obj)
                linked_obj.InsertUnder(groupNull)

        print("Grouped cloner '{}' with {} effector(s)".format(cloner.GetName(), len(effectors)))

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
