"""
Sets the preview range based on render settings or project time range.

Modifiers:
- No modifier: Sets preview range to match render settings
- Hold Alt: Sets preview range to match project's full time range (min to max time)
"""

import c4d

def get_key_mod():
    """Check for Alt key"""
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
            return True
    return False

def main():
    doc = c4d.documents.GetActiveDocument()
    if not doc:
        return

    if get_key_mod():
        # If Alt is held, use project min/max time
        start_time = doc[c4d.DOCUMENT_MINTIME]
        end_time = doc[c4d.DOCUMENT_MAXTIME]
    else:
        # Get the active render settings
        rd = doc.GetActiveRenderData()
        if not rd:
            return

        # Get frame range from render settings
        start_time = rd[c4d.RDATA_FRAMEFROM]
        end_time = rd[c4d.RDATA_FRAMETO]

    # Set preview range
    doc[c4d.DOCUMENT_LOOPMINTIME] = start_time
    doc[c4d.DOCUMENT_LOOPMAXTIME] = end_time
    
    # Set current time to start of range
    doc[c4d.DOCUMENT_TIME] = start_time

    # Update the timeline
    c4d.EventAdd()

if __name__ == '__main__':
    main()
