"""
Author: Mateo Vallejo
Version: 1.0.0
Description: Set project FPS to 24, 25 or 30.
"""
import c4d
from c4d import gui

def create_dropdown_menu(menu_entries, icons=None):
    entries = c4d.BaseContainer()
    for entry_id, label in menu_entries.items():
        if icons and entry_id in icons:
            label = icons[entry_id] + " " + label
        entries.SetString(entry_id, label)
    return gui.ShowPopupDialog(cd=None, bc=entries, x=c4d.MOUSEPOS, y=c4d.MOUSEPOS, flags=c4d.POPUP_RIGHT)

def set_fps(doc, fps):
    doc.SetFps(fps)
    rd = doc.GetActiveRenderData()
    if rd:
        rd[c4d.RDATA_FRAMERATE] = fps

def main():
    doc = c4d.documents.GetActiveDocument()
    if not doc:
        return

    fps_presets = {
        10: "24 FPS",
        11: "25 FPS",
        12: "30 FPS",
    }
    icons = {
        10: "&i37000&",
        11: "&i37000&",
        12: "&i37000&",
    }

    selected = create_dropdown_menu(fps_presets, icons)
    if selected is not None:
        fps_map = {10: 24, 11: 25, 12: 30}
        fps = fps_map.get(selected)
        if fps:
            set_fps(doc, fps)
            c4d.EventAdd()

if __name__ == '__main__':
    main()
