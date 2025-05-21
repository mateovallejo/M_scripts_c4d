"""
Author: Mateo Vallejo
Version: 1.0.0
Description-US: Script to set render output path from presets using a dropdown menu.
"""

import c4d
from c4d import gui
import os

def create_dropdown_menu(menu_entries, icons=None):
    """Creates and shows a dropdown menu in Cinema 4D."""
    entries = c4d.BaseContainer()
    for entry_id, label in menu_entries.items():
        if icons and entry_id in icons:
            label = icons[entry_id] + " " + label
        entries.SetString(entry_id, label)
    
    return gui.ShowPopupDialog(cd=None, bc=entries, x=c4d.MOUSEPOS, y=c4d.MOUSEPOS, flags=c4d.POPUP_RIGHT)

def set_render_path(path):
    """Sets the render output path in render settings"""
    rd = doc.GetActiveRenderData()
    if rd is None:
        return False
    
    rd[c4d.RDATA_PATH] = path
    doc.SetActiveRenderData(rd)
    return True

def main():
    # Get active document
    doc = c4d.documents.GetActiveDocument()
    
    # Define preset paths
    path_presets = {
        10: "../3D_Render/$prj/$prj",
        11: "../3D_Render/$take/$take",
        12: "../3D_Anim/$prj/$prj",
        13: "../3D_Anim/$take/$take",
        14: "../../Dailies/$take_$MM$DD",
        15: "../../Rnd/$prj/$prj_$camera_",
    }

    # Define icons for the menu
    icons = {
        10: "&i37000&",  # Render settings icon
        11: "&i37000&",
        12: "&i37000&",
        13: "&i37000&",
        14: "&i37000&",
        15: "&i37000&",
    }    
    
    # Show dropdown menu
    selected = create_dropdown_menu(path_presets, icons)
    
    # Handle selection
    if selected is not None:
        selected_path = path_presets.get(selected)
        if selected_path:
            if set_render_path(selected_path):
                c4d.EventAdd()

if __name__ == '__main__':
    main()
