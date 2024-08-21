"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Name-US:m_CameraFilter Toggle
Description-US:Align first selected object to second selected object.
"""

import c4d
from c4d import gui

def main():
    c4d.CallCommand(70000, 911) # Display Filter

if __name__=='__main__':
    main()
    c4d.EventAdd()