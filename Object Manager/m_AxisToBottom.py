"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US: Set axis to the bottom of selected object.
"""
import c4d

def main():
    doc = c4d.documents.GetActiveDocument()
    
    # Start the undo block.
    doc.StartUndo()
    
    # Get all selected objects
    selected_objects = doc.GetActiveObjects(0)
    
    for obj in selected_objects:
        # Add undo for the object before making changes.
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        
        # Get object's points in local space
        points = obj.GetAllPoints()
        if not points:
            continue  # Skip objects without editable points
        
        # Initialize bounding box with the first point
        minX = maxX = points[0].x
        minY = maxY = points[0].y
        minZ = maxZ = points[0].z

        # Calculate the bounds of the object's geometry
        for pt in points:
            if pt.x < minX: minX = pt.x
            if pt.x > maxX: maxX = pt.x
            if pt.y < minY: minY = pt.y
            if pt.y > maxY: maxY = pt.y
            if pt.z < minZ: minZ = pt.z
            if pt.z > maxZ: maxZ = pt.z

        # Compute center on X and Z, and bottom on Y
        centerX = (minX + maxX) * 0.5
        centerZ = (minZ + maxZ) * 0.5

        # Create the shift vector (bottom center)
        shift = c4d.Vector(centerX, minY, centerZ)

        # Adjust all points so that bottom center aligns with the origin
        newPoints = [pt - shift for pt in points]
        obj.SetAllPoints(newPoints)
        obj.Message(c4d.MSG_UPDATE)

        # Compensate the object's world position so it doesn't move in the scene
        obj.SetRelPos(obj.GetRelPos() + shift)

    # End the undo block.
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
