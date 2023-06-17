def addTrail(desiredLength: int, yourString: str, symbol: str) -> str:
    sizeExt = ''
    count = 0
    
    while (count+len(yourString)<desiredLength):
        sizeExt+=symbol
        count+=1
        print('stuck in add trail')

    return sizeExt+yourString