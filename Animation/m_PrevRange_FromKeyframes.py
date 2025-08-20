"""
Sets the preview range based on selected objects' keyframe range.

Modifiers:
- No modifier: Sets preview range to match selected objects' keyframe range
- Hold Alt: Sets preview range to match project's full time range (min to max time)
"""

import c4d

def get_key_mod():
    """Check for Alt key"""
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
            return True
    return False

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

def get_selected_objects_frame_range(doc):
    """Gets the overall frame range for all selected objects"""
    objects = doc.GetActiveObjects(0)  # 0 = no flags; get all selected
    if not objects:
        return None

    all_frames = []
    for obj in objects:
        keyframe_range = get_keyframe_range(obj, doc)
        if keyframe_range:
            all_frames.extend(keyframe_range)

    if not all_frames:
        return None

    fps = doc.GetFps()
    return (
        c4d.BaseTime(min(all_frames), fps),
        c4d.BaseTime(max(all_frames), fps)
    )

def main():
    doc = c4d.documents.GetActiveDocument()
    if not doc:
        return

    if get_key_mod():
        # If Alt is held, use project min/max time
        start_time = doc[c4d.DOCUMENT_MINTIME]
        end_time = doc[c4d.DOCUMENT_MAXTIME]
    else:
        # Get frame range from selected objects
        frame_range = get_selected_objects_frame_range(doc)
        if not frame_range:
            c4d.gui.MessageDialog("No keyframes found in selected objects.")
            return
        
        start_time, end_time = frame_range

    # Set preview range
    doc[c4d.DOCUMENT_LOOPMINTIME] = start_time
    doc[c4d.DOCUMENT_LOOPMAXTIME] = end_time
    
    # Set current time to start of range
    doc[c4d.DOCUMENT_TIME] = start_time

    # Update the timeline
    c4d.EventAdd()

if __name__ == '__main__':
    main()
