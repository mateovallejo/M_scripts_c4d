"""
Author: Mateo Vallejo
Website: https://mateovallejo.com
Version: 1.0.0
Description-US:Toggles the visibility of the camera grid.
"""    
import c4d

def ToggleCameraGrid():
    # Obtener la cámara activa en la vista
    camera = doc.GetActiveBaseDraw().GetSceneCamera(doc)
    

    # Comprobar el estado actual del grid y alternarlo
    current_state = camera[c4d.RSCAMERAOBJECT_LAYOUTHELP_DRAW_GRID_ENABLE]
    camera[c4d.RSCAMERAOBJECT_LAYOUTHELP_DRAW_GRID_ENABLE] = not current_state

    # Actualizar Cinema 4D para reflejar el cambio
    c4d.EventAdd()

if __name__ == "__main__":
    ToggleCameraGrid()
