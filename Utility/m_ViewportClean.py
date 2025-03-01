"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Toggles visibility of various viewport elements.
"""

import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    
    c4d.CallCommand(18175) # Workplane
    c4d.CallCommand(18177) # World Axis
    c4d.CallCommand(18171) # Light
    c4d.CallCommand(18170) # Camera
    c4d.CallCommand(18192) # Field
    c4d.CallCommand(18169) # Deformer

if __name__ == '__main__':
    main()