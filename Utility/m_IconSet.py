"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US: Changes the icon of selected objects in Cinema 4D.
"""

import c4d
from c4d import gui

def create_dropdown_menu(menu_entries, icons=None):
    """
    Creates and shows a dropdown menu in Cinema 4D.

    Args:
        menu_entries (dict): Dictionary with menu entries where:
            - Key: Integer ID for the menu item (10-99)
            - Value: String label for the menu item
        icons (dict, optional): Dictionary with icon IDs where:
            - Key: Same integer ID as in menu_entries
            - Value: String icon ID (e.g., "&i18171&")

    Returns:
        int: The selected menu item ID, or None if cancelled
    """
    # Create the container for menu entries
    entries = c4d.BaseContainer()

    # Add entries to the container
    for entry_id, label in menu_entries.items():
        # If icons are provided, prepend the icon to the label
        if icons and entry_id in icons:
            label = icons[entry_id] + " " + label
        entries.SetString(entry_id, label)

    # Show the popup dialog at mouse position
    result = gui.ShowPopupDialog(
        cd=None,
        bc=entries,
        x=c4d.MOUSEPOS,
        y=c4d.MOUSEPOS,
        flags=c4d.POPUP_RIGHT
    )

    return result

def change_object_icon(doc, obj, icon_id):
    """
    Changes the icon of an object in Cinema 4D.

    Args:
        doc: The active document
        obj: The object to change the icon of
        icon_id: The ID of the icon to apply
    """
    # Set the icon file parameter
    obj.SetParameter(c4d.ID_BASELIST_ICON_FILE, str(icon_id), c4d.DESCFLAGS_SET_0)
    # Enable icon colorization
    obj[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2
    # Update the object
    obj.Message(c4d.MSG_UPDATE)

def main():
    # Get the active document
    doc = c4d.documents.GetActiveDocument()

    # Get selected objects
    selected_objects = doc.GetActiveObjects(0)

    if not selected_objects:
        gui.MessageDialog("Please select at least one object.")
        return

    # Define menu entries with icon names
    menu_items = {
        8: "Default",
        9: "Folder",
        10: "Light",
        11: "Spotlight",
        12: "Planet",
        13: "Octagon",
        14: "Circle",
        15: "Star",
        16: "TreeLeaf",
        17: "Pencil",
        18: "Cam",
        19: "Text",
        20: "Locator",
        21: "Pyramid",
        22: "Text A",
        23: "Chain",
        24: "Axis",
        25: "PixelScreen",
        26: "Polygon",
        27: "Hand",
        28: "Joint",
        29: "Matrix",
        30: "Sculpt",
        31: "Grass",
        32: "Stage"
    }

    # Define icon IDs
    icon_items = {
        8: "",
        9: "&i1052838&",
        10: "&i202537&",
        11: "&i200000031&",
        12: "&i17107&",
        13: "&i1058519&",
        14: "&i1058513&",
        15: "&i1058512&",
        16: "&i13861&",
        17: "&i13740&",
        18: "&i18170&",
        19: "&i1059743&",
        20: "&i1058512&",
        21: "&i1058523&",
        22: "&i1060484&",
        23: "&i1023416&",
        24: "&i1058521&",
        25: "&i17551&",
        26: "&i18165&",
        27: "&i1022956&",
        28: "&i18185&",
        29: "&i440000235&",
        30: "&i431000214&",
        31: "&i1028462&",
        32: "&i5136&"
    }

    # Show the menu and get the result
    selected = create_dropdown_menu(menu_items, icon_items)

    if selected is not None:
        # Start undo
        doc.StartUndo()

        # Get the selected icon ID (remove the &i and & from the icon string)
        icon_id = icon_items[selected].replace("&i", "").replace("&", "")

        # Change icon for each selected object
        for obj in selected_objects:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            change_object_icon(doc, obj, icon_id)

        # End undo
        doc.EndUndo()
        # Update the scene
        c4d.EventAdd()

if __name__ == '__main__':
    main()