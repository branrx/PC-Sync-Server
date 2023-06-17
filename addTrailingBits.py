#   adds extra bits  to start of command so that 8 bytes are sent on every 
#   command example, if addTrail(8, 1, 0), string sent should 
#   be 00000001 
def addTrail(desiredLength: int, yourString: str, symbol: str) -> str:
    sizeExt = ''
    count = 0
    
    while (count+len(yourString)<desiredLength):
        sizeExt+=symbol
        count+=1

    return sizeExt+yourString