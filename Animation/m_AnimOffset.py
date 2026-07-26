"""
Offset selected animation keyframes by a custom amount of frames.
Usage:
- Select the relevant objects and/or keyframes in the animation editor.
- Run the script.
- Enter the frame offset in the popup window.
- Positive values move keys forward, negative values move them backward.
"""
import c4d

def get_frame_offset():
    """Show a popup input dialog and return the entered frame offset as a float."""
    offset_text = c4d.gui.InputDialog("Frame offset")
    if offset_text is None:
        return None
    try:
        offset = float(offset_text)
    except (TypeError, ValueError):
        c4d.gui.MessageDialog("Please enter a valid number of frames.")
        return None
    return offset

def main():
    doc = c4d.documents.GetActiveDocument()
    if not doc:
        return

    offset_frames = get_frame_offset()
    if offset_frames is None:
        return
    if offset_frames == 0:
        c4d.gui.MessageDialog("Offset is 0, nothing to change.")
        return

    selected_objects = doc.GetActiveObjects(0)
    if not selected_objects:
        c4d.gui.MessageDialog("Please select at least one object with animation.")
        return

    fps = doc.GetFps()
    offset_time = c4d.BaseTime(offset_frames, fps)

    doc.StartUndo()
    try:
        changed = False
        for obj in selected_objects:
            if not obj:
                continue
            track = obj.GetFirstCTrack()
            while track:
                curve = track.GetCurve()
                if curve:
                    key_count = curve.GetKeyCount()
                    if key_count > 0:
                        # Register undo for this track before modifying its keys
                        doc.AddUndo(c4d.UNDOTYPE_CHANGE, track)
                        for i in range(key_count):
                            key = curve.GetKey(i)
                            current_time = key.GetTime()
                            key.SetTime(curve, current_time + offset_time)
                            changed = True
                track = track.GetNext()
        if not changed:
            c4d.gui.MessageDialog("No animation keys were found to offset.")
            return
        c4d.EventAdd()
    finally:
        doc.EndUndo()

if __name__ == '__main__':
    main()