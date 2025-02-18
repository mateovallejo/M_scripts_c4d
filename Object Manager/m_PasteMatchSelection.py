"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US: Paste object and match its coordinates to current selected object.
"""

import c4d
from c4d import plugins

def main():
    doc = c4d.documents.GetActiveDocument()
    
    # Check that there is a selected object (reference object)
    refObj = doc.GetActiveObject()
    if refObj is None:
        c4d.gui.MessageDialog("Select the reference object before pasting.")
        return
    
    # Save the global matrix of the reference object
    refMg = refObj.GetMg()
    
    # Helper function to access preferences
    def prefs(id):
        return plugins.FindPlugin(id, c4d.PLUGINTYPE_PREFS)
    
    # Access the 'Paste At' preference
    pref = prefs(465001620)
    if not pref:
        c4d.gui.MessageDialog("Could not access the paste preference.")
        return
    
    # Save the default behavior and change the preference to paste "next to" (according to the desired configuration)
    temp = pref[c4d.PREF_INTERFACE_PASTEAT]
    pref[c4d.PREF_INTERFACE_PASTEAT] = 2  # Temporary adjustment (according to your reference script)
    
    # Execute the Paste command
    c4d.CallCommand(12108)  # Paste
    
    # Restore the original preference
    pref[c4d.PREF_INTERFACE_PASTEAT] = temp
    
    # Get the pasted object, which becomes the active object
    pastedObj = doc.GetActiveObject()
    if pastedObj is None:
        c4d.gui.MessageDialog("Could not get the pasted object.")
        return
    
    # Adjust the global matrix so that it matches the reference object's matrix
    pastedObj.SetMg(refMg)
    
    c4d.EventAdd()

if __name__=='__main__':
    main()
