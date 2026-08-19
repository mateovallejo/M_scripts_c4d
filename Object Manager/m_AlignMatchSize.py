"""
Author: Mateo Vallejo
Website:
Version: 1.1.0
Name-US: m_AlignMatchSize
Description-US: Align all selected objects to the last selected object's position and
                orientation, and uniformly scale them so their largest dimension
                matches the target's largest dimension. Proportions are always
                preserved (no stretching/deforming).
"""

import c4d

def get_local_bbox_size(obj):
    """
    Returns the bounding box size (c4d.Vector) of obj in its own local/object
    space, i.e. independent of obj's own matrix scale. Uses the object's cache
    for generators so it reflects the actual generated geometry.
    """
    src = obj.GetCache() or obj
    rad = src.GetRad()
    return rad * 2.0

def safe_div(a, b):
    return a / b if abs(b) > 1e-8 else 1.0

def main():
    doc = c4d.documents.GetActiveDocument()

    # Retrieve selected objects in selection order if available
    if hasattr(c4d, 'GETACTIVEOBJECTFLAGS_SELECTIONORDER'):
        selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    else:
        selected = doc.GetActiveObjects(0)

    # Check that there are at least two selected objects
    if not selected or len(selected) < 2:
        print("Please select at least two objects")
        return

    # The last selected object is the target for alignment and size matching
    target_obj = selected[-1]
    target_mg = target_obj.GetMg()

    # Target's world-space bounding box size, measured along its own local axes
    target_local_size = get_local_bbox_size(target_obj)
    target_scale = c4d.Vector(target_mg.v1.GetLength(), target_mg.v2.GetLength(), target_mg.v3.GetLength())
    target_world_size = c4d.Vector(
        target_local_size.x * target_scale.x,
        target_local_size.y * target_scale.y,
        target_local_size.z * target_scale.z
    )
    target_max_size = max(target_world_size.x, target_world_size.y, target_world_size.z)

    # Normalized direction vectors from the target's matrix (its orientation)
    dir1 = target_mg.v1.GetNormalized()
    dir2 = target_mg.v2.GetNormalized()
    dir3 = target_mg.v3.GetNormalized()

    doc.StartUndo()

    for obj in selected[:-1]:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

        obj_local_size = get_local_bbox_size(obj)
        obj_max_size = max(obj_local_size.x, obj_local_size.y, obj_local_size.z)

        s = safe_div(target_max_size, obj_max_size)
        new_scale = c4d.Vector(s, s, s)

        new_mg = c4d.Matrix()
        new_mg.off = target_mg.off
        new_mg.v1 = dir1 * new_scale.x
        new_mg.v2 = dir2 * new_scale.y
        new_mg.v3 = dir3 * new_scale.z

        obj.SetMg(new_mg)

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()