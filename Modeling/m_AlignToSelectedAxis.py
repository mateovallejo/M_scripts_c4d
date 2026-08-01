"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Name-US: m_AlignAxisToLastSelected
Description-US: Aligns the axis (pivot position and orientation) of selected objects to the
    last selected object's axis, without moving the actual geometry (points/polygons) or
    children in world space.
Note: Currently does not support normal tags (same limitation as AR_AxisToOrigin).
"""
import c4d

def AlignAxis(obj, targetMg):
    """Moves obj's axis to targetMg without moving its geometry or children in world space."""
    doc = obj.GetDocument()
    matOld = obj.GetMg()  # Store object's original global matrix

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

    # Store children's global matrices BEFORE moving the axis
    children = obj.GetChildren()
    childrenMat = [child.GetMg() for child in children]

    obj.SetMg(targetMg)  # Move the axis to the target matrix
    mat = obj.GetMg()    # New global matrix

    # Compensate points so geometry doesn't move (only applies to point objects)
    if obj.CheckType(c4d.Opoint):
        cnt = obj.GetPointCount()
        isBezier = obj.CheckType(c4d.Ospline) and obj[c4d.SPLINEOBJECT_TYPE] == c4d.SPLINEOBJECT_TYPE_BEZIER
        for i in range(cnt):
            pos = obj.GetPoint(i)
            posGlobal = matOld * pos
            obj.SetPoint(i, ~mat * posGlobal)
            if isBezier:
                tan = obj.GetTangent(i)
                tan_l = tan['vl'] + pos
                tan_r = tan['vr'] + pos
                tan_l_glo = matOld * tan_l
                tan_r_glo = matOld * tan_r
                posNew = obj.GetPoint(i)
                tan_l_new = ~mat * tan_l_glo - posNew
                tan_r_new = ~mat * tan_r_glo - posNew
                obj.SetTangent(i, tan_l_new, tan_r_new)
        obj.Message(c4d.MSG_UPDATE)

    # Restore children to their original world-space transform
    for child, childMgOld in zip(children, childrenMat):
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)
        child.SetMg(childMgOld)

def main():
    doc = c4d.documents.GetActiveDocument()
    # Retrieve selected objects in selection order if available
    if hasattr(c4d, 'GETACTIVEOBJECTFLAGS_SELECTIONORDER'):
        selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    else:
        selected = doc.GetActiveObjects(0)

    if not selected or len(selected) < 2:
        print("Please select at least two objects")
        return

    # The last selected object is the target axis
    target_obj = selected[-1]
    target_mg = target_obj.GetMg()

    doc.StartUndo()
    for obj in selected[:-1]:
        AlignAxis(obj, target_mg)
    doc.EndUndo()

    c4d.EventAdd()

if __name__=='__main__':
    main()