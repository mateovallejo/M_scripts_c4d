import c4d

def main():
    # Set to "X", "Y", or "Z" to keep that axis unlocked
    axis = "Y"  # Change to "Y" or "Z" as needed

    # Lock the other two axes
    if axis.upper() == "X":
        c4d.CallCommand(12154)  # Lock Y
        c4d.CallCommand(12155)  # Lock Z
    elif axis.upper() == "Y":
        c4d.CallCommand(12153)  # Lock X
        c4d.CallCommand(12155)  # Lock Z
    elif axis.upper() == "Z":
        c4d.CallCommand(12153)  # Lock X
        c4d.CallCommand(12154)  # Lock Y

if __name__ == '__main__':
    main()