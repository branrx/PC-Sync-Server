
#   returns a file as dict containing: data, size, filename
#   needs to return list of bytearray, size, filename
def getAsBytes(filepath) -> dict:
    #   gets file name
    fileName = filepath.split('//')[-1]
    
    #   get filedata as bytes
    audioFile = open(filepath, 'rb')
    audioFileB = open(filepath, 'rb')
    fileSizeB =  audioFileB.read()
    fileSizeB = len(fileSizeB)

    #   gets file size
    fileSizeAsString = str(fileSizeB)
    fileSizeB = int.to_bytes(fileSizeB, 10, 'big')

    #   read file into bytearray
    data = audioFile.read()
    fileData = data
    
    return {'filename': fileName, 'data': fileData, 'size': fileSizeAsString}
