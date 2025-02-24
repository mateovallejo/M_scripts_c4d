import c4d

def main():
    # Get the active BaseDraw, which is used to retrieve the scene camera.
    bd = doc.GetActiveBaseDraw()
    cam = bd.GetSceneCamera(doc)
    if cam is None:
        c4d.gui.MessageDialog("No active camera found. Please set a scene camera first.")
        return

    # Get the active (selected) object.
    selected_obj = doc.GetActiveObject()
    if selected_obj is None:
        c4d.gui.MessageDialog("No object selected. Please select an object to focus on.")
        return

    # Set the camera's target object parameter.
    cam[c4d.RSCAMERAOBJECT_TARGETOBJECT] = selected_obj

    # Update the Cinema 4D scene.
    c4d.EventAdd()

if __name__=='__main__':
    main()
