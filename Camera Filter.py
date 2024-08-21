import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    c4d.CallCommand(70000, 911) # Display Filter

if __name__=='__main__':
    main()
    c4d.EventAdd()
