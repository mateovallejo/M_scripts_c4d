"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US: Flatten selected polygons in the active object. ALT: Align with camera view.
"""

import c4d
import typing

doc: c4d.documents.BaseDocument  # The currently active document.
op: typing.Optional[c4d.BaseObject]  # The selected object within that active document. Can be None.


def AssertType(item: any, t: typing.Type) -> None:
    """Asserts the type of the item."""
    if not isinstance(item, t):
        raise TypeError(f"Expected {t} for {item}.")


def GetMean(collection: typing.Collection) -> typing.Any:
    """Returns the arithmetic mean of the collection."""
    return sum(collection) * (1. / len(collection))


def ProjectIntoPlane(p: c4d.Vector, q: c4d.Vector, normal: c4d.Vector) -> c4d.Vector:
    """Projects the point p orthogonally into the plane defined by q and normal."""
    AssertType(p, c4d.Vector)
    AssertType(q, c4d.Vector)
    AssertType(normal, c4d.Vector)

    distance = (p - q) * normal
    return p - normal * distance


def GetPolygonNormal(points: typing.Collection[c4d.Vector]) -> c4d.Vector:
    """Returns the normal of the polygon defined by the passed points."""
    AssertType(points, (list, tuple))
    if len(points) not in (3, 4):
        raise RuntimeError(f"Invalid length for: {points}")

    count = len(points)
    vertexNormals = []

    for index in range(count):
        h = points[index - 1] if index > 0 else points[count - 1]
        i = points[index]
        j = points[index + 1] if index < (count - 1) else points[0]
        e1, e2 = (h - i), (i - j)
        vertexNormals.append(e1 % e2)

    return ~GetMean(vertexNormals)


def isAltPressed() -> bool:
    """
    Returns True if the ALT key is pressed.
    """
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        if qualifier & c4d.QALT:
            return True
    return False



def GetCameraViewNormal(doc: c4d.documents.BaseDocument) -> c4d.Vector:
    """Returns the view normal from the active camera (the negative z-axis)."""
    bd = doc.GetActiveBaseDraw()
    if bd is None:
        raise RuntimeError("No active base draw found.")

    cam = bd.GetSceneCamera(doc)
    if cam is None:
        cam = bd.GetEditorCamera()

    mg = cam.GetMg()
    viewNormal = -mg.v3.GetNormalized()  # The negative z-axis typically represents the forward view.
    return viewNormal


def FlattenPolygonObjectSelection(node: c4d.PolygonObject, strength: float, doc: c4d.documents.BaseDocument) -> c4d.PolygonObject:
    """Projects the selected polygons in node into the mean plane of the selection or into a camera-aligned plane.

    If the ALT key is pressed, the projection plane is aligned to the current camera view.
    Otherwise, the plane is computed as the mean plane of the selected polygon vertices.

    Args:
        strength: The strength value in the interval [0, 1] with which the projection should be applied.
        doc: The current document, used for retrieving the active camera.

    Returns:
        The 'flattened' object.
    """
    AssertType(node, c4d.PolygonObject)
    AssertType(strength, (float, int))
    strength = c4d.utils.Clamp(0.0, 1.0, strength)

    nodeDoc = node.GetDocument()
    if nodeDoc is None:
        raise RuntimeError(f"'{node.GetName()}' is not attached to a document.")

    points = node.GetAllPoints()
    polygons = node.GetAllPolygons()
    polygonCount = len(polygons)

    if polygonCount < 1:
        raise RuntimeError(f"'{node.GetName()}' does not contain any polygons.")

    baseSelect = node.GetPolygonS()
    polygonSelection = baseSelect.GetAll(polygonCount)
    selectedPolygonIds = [i for i, v in enumerate(polygonSelection) if v]
    selectedPolygons = [polygons[i] for i in selectedPolygonIds]

    if not selectedPolygons:
        raise RuntimeError(f"'{node.GetName()}' does not contain any selected polygons.")

    selectedPointIds = list({p for cpoly in selectedPolygons
                             for p in [cpoly.a, cpoly.b, cpoly.c, cpoly.d]})
    selectedPoints = [points[i] for i in selectedPointIds]

    # Determine the projection normal:
    # If ALT is pressed, align with the current camera view.
    # Otherwise, compute the mean normal from the selected polygons.
    if isAltPressed():
        meanNormal = GetCameraViewNormal(doc)
    else:
        polygonNormals = [
            GetPolygonNormal([points[cpoly.a], points[cpoly.b], points[cpoly.c]]
                             if cpoly.IsTriangle() else
                             [points[cpoly.a], points[cpoly.b], points[cpoly.c], points[cpoly.d]])
            for cpoly in selectedPolygons
        ]
        meanNormal = ~GetMean(polygonNormals)

    meanPoint = GetMean(selectedPoints)

    for pid in selectedPointIds:
        p = ProjectIntoPlane(points[pid], meanPoint, meanNormal)
        points[pid] = c4d.utils.MixVec(points[pid], p, strength)

    if not nodeDoc.StartUndo():
        raise RuntimeError("Could not open undo stack.")

    if not nodeDoc.AddUndo(c4d.UNDOTYPE_CHANGE, node):
        raise RuntimeError("Could not add undo item.")

    node.SetAllPoints(points)
    node.Message(c4d.MSG_UPDATE)

    if not nodeDoc.EndUndo():
        raise RuntimeError("Could not close undo stack.")

    return node


def main(doc: c4d.documents.BaseDocument, op: typing.Optional[c4d.BaseObject]) -> None:
    """Runs the example.

    Args:
        doc: The active document.
        op: The selected object in doc. Must be a polygon object.
    """
    if not isinstance(op, c4d.PolygonObject):
        raise RuntimeError("No polygon object selected.")

    node = op

    # Pass the document to the flatten function so it can query the active camera.
    FlattenPolygonObjectSelection(node, 1.0, doc)

    doc.SetMode(c4d.Mpolygons)
    doc.SetActiveObject(node, c4d.SELECTION_NEW)
    c4d.EventAdd()


if __name__ == '__main__':
    c4d.CallCommand(13957)  # Clear the console.
    main(doc, op)
