"""
Go to end PreviewRange Frame

"""

import c4d

def main():
    doc = c4d.documents.GetActiveDocument()

    start_time = doc[c4d.DOCUMENT_LOOPMINTIME]

    # Set current time to end of range
    doc[c4d.DOCUMENT_TIME] = start_time

    # Update the timeline
    c4d.EventAdd()

if __name__ == '__main__':
    main()