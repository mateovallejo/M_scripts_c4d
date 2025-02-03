import c4d
from c4d import documents

def main():
    doc = documents.GetActiveDocument()
    if not doc:
        return
    
    doc.StartUndo()  # Start Undo Block
    
    # Create Null objects to group Lights and Geometry
    lights_null = c4d.BaseObject(c4d.Onull)
    lights_null.SetName("Lights")
    doc.InsertObject(lights_null)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, lights_null)
    
    geometry_null = c4d.BaseObject(c4d.Onull)
    geometry_null.SetName("Geometry")
    doc.InsertObject(geometry_null)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, geometry_null)
    
    # Iterate over all objects in the scene
    obj = doc.GetFirstObject()
    while obj:
        next_obj = obj.GetNext()  # Store next object before modifying hierarchy
        obj_type = obj.GetType()
        
        # Check if object is a Light
        if c4d.Obase in obj.GetUpM():
            obj.InsertUnder(lights_null)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        # Check if object is a Primitive or a Polygon Object
        elif obj_type in [c4d.Ocube, c4d.Osphere, c4d.Ocylinder, c4d.Ocone, c4d.Oplane, c4d.Opolygon]:
            obj.InsertUnder(geometry_null)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        
        obj = next_obj  # Move to next object
    
    doc.EndUndo()  # End Undo Block
    c4d.EventAdd()
    
if __name__ == '__main__':
    main()
