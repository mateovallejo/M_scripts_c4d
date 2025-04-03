"""
Author: Mateo Vallejo
Version: 1.0.1
Description: Selects vertices with a specific number of connected edges based on user selection.
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

def main():
    # Get the currently active object.
    doc = c4d.documents.GetActiveDocument()
    obj = doc.GetActiveObject()
    if obj is None:
        c4d.gui.MessageDialog("No object selected.")
        return

    # Ensure the object is a polygon object.
    if not obj.CheckType(c4d.Opolygon):
        c4d.gui.MessageDialog("Selected object is not a polygon object.")
        return

    # Show dropdown menu for edge count selection
    menu_items = {
        2: "2 Edge Vertices",
        3: "3 Edge Vertices",
        4: "4 Edge Vertices",
        5: "5 Edge Vertices",
        6: "6 Edge Vertices",
        7: "7 Edge Vertices"
    }
    
    selected_edge_count = create_dropdown_menu(menu_items)
    
    # If user cancelled the dropdown, exit the function
    if selected_edge_count is None:
        return
    
    # Retrieve all points and polygons from the object.
    points = obj.GetAllPoints()
    polys = obj.GetAllPolygons()
    numPoints = len(points)

    # Create a list of sets to store connected vertex indices for each vertex.
    vertexEdges = [set() for _ in range(numPoints)]
    
    # Loop through each polygon to determine connectivity.
    for poly in polys:
        # Get the vertex indices for the polygon.
        indices = [poly.a, poly.b, poly.c]
        # If the polygon is a quad, add the fourth vertex.
        if not poly.IsTriangle():
            indices.append(poly.d)

        count = len(indices)
        # Loop over each edge in the polygon and add the connection for both vertices.
        for i in range(count):
            a = indices[i]
            b = indices[(i + 1) % count]
            vertexEdges[a].add(b)
            vertexEdges[b].add(a)

    # Create a new point selection tag.
    selTag = c4d.BaseTag(c4d.Tpointselection)
    selTag.SetName(f"{selected_edge_count} Edge Vertices")
    obj.InsertTag(selTag)
    
    # Get the selection container from the new tag and clear any existing selections.
    pointSel = selTag.GetBaseSelect()
    pointSel.DeselectAll()
    
    # Select vertices that have the selected number of connected edges.
    for i, connected in enumerate(vertexEdges):
        if len(connected) == selected_edge_count:
            pointSel.Select(i)

    # Refresh the scene.
    c4d.EventAdd()

if __name__=='__main__':
    main()
