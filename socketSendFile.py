
#   needs to return list of bytearray, size, filename
def getAsBytes(filepath) -> dict:
    #   file name
    fileName = filepath.split('//')[-1]

    #users[name].send(fileIndex.encode())

    #time.sleep(2)

    #   send the size of the file
    #   ex. 2**src dir\\Holy Ten - Pfumo(MP3_320K).mp3
    
    audioFile = open(filepath, 'rb')
    audioFileB = open(filepath, 'rb')
    fileSizeB =  audioFileB.read()
    fileSizeB = len(fileSizeB)

    #   file size
    fileSizeAsString = str(fileSizeB)
    fileSizeB = int.to_bytes(fileSizeB, 10, 'big')

    
    #users[name].send(fileSizeB)

    #   read file into bytearray
    data = audioFile.read()
    fileData = data
    #users[name].sendall(data)
    
    return {'filename': fileName, 'data': fileData, 'size': fileSizeAsString}
