"""
Cycles through takes in Cinema 4D, moving to the next or previous take in the hierarchy.
If the current take is the last one, it cycles back to the first take after Main.

Modifiers:
- Hold Shift: Cycle in reverse order
- Hold Alt: Also set preview range to match take's render settings
- Hold Ctrl: Cycle in reverse order and update preview range

Written for Maxon Cinema 4D 2025
"""

import c4d

def get_key_mod():
    """Check for keyboard modifiers (Shift, Alt, and Ctrl keys)"""
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qual = bc[c4d.BFM_INPUT_QUALIFIER]
        if qual & c4d.QCTRL:
            return 'Ctrl'
        elif qual & c4d.QSHIFT:
            return 'Shift'
        elif qual & c4d.QALT:
            return 'Alt'
    return 'None'

def set_preview_range(doc, take):
    """Set preview range based on take's render settings"""
    if not take or take.IsMain():
        return

    # Get render data for the take
    rd = take.GetRenderData(doc.GetTakeData())
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

def get_all_takes(main_take):
    """Collect all takes in a list for easier cycling"""
    takes = []
    take = main_take.GetDown()  # Get first take after Main
    while take:
        takes.append(take)
        take = take.GetNext()
    return takes

def main():
    # Get active document and its take data
    doc = c4d.documents.GetActiveDocument()
    if doc is None:
        return

    take_data = doc.GetTakeData()
    if take_data is None:
        c4d.gui.MessageDialog("Failed to retrieve take data.")
        return

    # Get main take and verify there are child takes
    main_take = take_data.GetMainTake()
    if main_take is None:
        return

    # Collect all takes
    takes = get_all_takes(main_take)
    if not takes:
        c4d.gui.MessageDialog("No takes found in the document.")
        return

    # Get current take
    current_take = take_data.GetCurrentTake()
    key_mod = get_key_mod()
    cycle_reverse = key_mod in ['Shift', 'Ctrl']

    if current_take is None or current_take.IsMain():
        # If we're on main take or no current take, start with first or last take depending on direction
        next_take = takes[-1] if cycle_reverse else takes[0]
    else:
        try:
            current_index = takes.index(current_take)
            if cycle_reverse:
                # Cycle backwards
                next_take = takes[current_index - 1] if current_index > 0 else takes[-1]
            else:
                # Cycle forwards
                next_take = takes[(current_index + 1) % len(takes)]
        except ValueError:
            # If current take not found in list, start with first
            next_take = takes[0]

    # Switch to the next take
    take_data.SetCurrentTake(next_take)

    # Check if we should update preview range
    if key_mod in ['Alt', 'Ctrl']:
        set_preview_range(doc, next_take)

    # Refresh the viewport
    c4d.EventAdd()

    # Show feedback to user (optional - comment out if not needed)
    #feedback = f"Switched to take: {next_take.GetName()}"
    #if key_mod in ['Alt', 'Ctrl']:
        #feedback += " (Preview range updated)"
    #c4d.gui.MessageDialog(feedback)

if __name__ == '__main__':
    main()