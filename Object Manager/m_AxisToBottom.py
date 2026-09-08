"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Name-US: m_AxisToBottom
Description-US: Aligns the axis (pivot position) of selected object(s) to their
    minimum Y point (bottom of the bounding box), without moving the actual
    geometry (points/polygons) or children in world space.
Note: Currently does not support normal tags (same limitation as AR_AxisToOrigin).
"""
import c4d


def GetMinYGlobal(obj):
    """
    Returns the minimum global Y value of obj.
    Uses editable points when available (including the cache of generator
    objects), otherwise falls back to the object's bounding box.
    """
    mg = obj.GetMg()

    point_obj = obj
    if not obj.CheckType(c4d.Opoint):
        cache = obj.GetCache()
        if cache is not None and cache.CheckType(c4d.Opoint):
            point_obj = cache

    if point_obj.CheckType(c4d.Opoint):
        points = point_obj.GetAllPoints()
        if points:
            point_mg = point_obj.GetMg() if point_obj != obj else mg
            return min((point_mg * p).y for p in points)

    # Fallback: use the object's bounding box (covers primitives, etc.)
    mp = obj.GetMp()
    rad = obj.GetRad()
    ys = [(mg * c4d.Vector(mp.x, mp.y - rad.y, mp.z)).y,
          (mg * c4d.Vector(mp.x, mp.y + rad.y, mp.z)).y]
    return min(ys)


def AlignAxisToMinY(obj, doc):
    """Moves obj's axis down to its minimum Y point without moving its
    geometry or children in world space."""
    matOld = obj.GetMg()  # Store object's original global matrix

    minY = GetMinYGlobal(obj)

    # Target matrix: same orientation/scale/X/Z, only Y changes to minY.
    targetMg = c4d.Matrix(matOld)
    targetMg.off = c4d.Vector(matOld.off.x, minY, matOld.off.z)

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

    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not selected:
        c4d.gui.MessageDialog("Please select at least one object.")
        return

    doc.StartUndo()
    for obj in selected:
        AlignAxisToMinY(obj, doc)
    doc.EndUndo()

    c4d.EventAdd()


if __name__ == '__main__':
    main()
