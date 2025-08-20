import c4d

# Global variables
CAMERA_TYPES = [5103, 1057516]  # Camera types in Cinema 4D

def get_keyframe_range(obj, doc):
    """Returns the first and last frame where the object has animation keyframes."""
    if not obj:
        return None

    fps = doc.GetFps()
    frames = []

    track = obj.GetFirstCTrack()
    while track:
        curve = track.GetCurve()
        if curve:
            for i in range(curve.GetKeyCount()):
                key = curve.GetKey(i)
                frame = key.GetTime().GetFrame(fps)
                frames.append(frame)
        track = track.GetNext()

    if not frames:
        return None

    return min(frames), max(frames)

def create_render_setting_for_object(doc, obj, first_frame, last_frame, parent_rd):
    """Creates a render setting and matching take named after the object and frame range."""
    if parent_rd:
        new_rd = parent_rd.GetClone()
    else:
        new_rd = c4d.documents.RenderData()

    obj_name = obj.GetName()
    setting_name = f"{obj_name}: {first_frame}f–{last_frame}f"
    new_rd.SetName(setting_name)

    new_rd[c4d.RDATA_FRAMESEQUENCE] = c4d.RDATA_FRAMESEQUENCE_MANUAL
    new_rd[c4d.RDATA_FRAMEFROM] = c4d.BaseTime(first_frame, doc.GetFps())
    new_rd[c4d.RDATA_FRAMETO] = c4d.BaseTime(last_frame, doc.GetFps())

    doc.InsertRenderData(new_rd)

    # Create a matching take and link it to the render setting
    take_data = doc.GetTakeData()
    if take_data:
        main_take = take_data.GetMainTake()
        child_take = main_take.GetDown()  # Get first child take
        new_take = take_data.AddTake("", main_take, child_take)  # Add take after existing ones
        new_take.SetName(setting_name)
        new_take.SetRenderData(take_data, new_rd)  # Link the take to its render setting
        
        # If the object is a camera, set it as the active camera for this take
        if obj.GetType() in CAMERA_TYPES:
            new_take.SetCamera(take_data, obj)
            
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, new_take)  # Add undo for creating a take

def main():
    doc = c4d.documents.GetActiveDocument()
    objects = doc.GetActiveObjects(0)  # 0 = no flags; get all selected
    parent_rd = doc.GetActiveRenderData()

    if not objects:
        c4d.gui.MessageDialog("No objects selected.")
        return

    doc.StartUndo()

    count_created = 0

    for obj in objects:
        keyframe_range = get_keyframe_range(obj, doc)
        if keyframe_range:
            first_frame, last_frame = keyframe_range
            create_render_setting_for_object(doc, obj, first_frame, last_frame, parent_rd)
            count_created += 1

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()