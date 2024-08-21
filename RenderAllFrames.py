import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    renderdata()[c4d.RDATA_FRAMESEQUENCE] = 2

if __name__=='__main__':
    main()
