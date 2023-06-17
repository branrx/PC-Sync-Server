import directory_crawler as dc

#   enumerates the directory, gets files
#   creates txt reprenting files present
#   returns nothing
def getFiles(filename, path, extensions):
    #   get all files in dest dir
    files, paths = dc.getFiles(path=path, extensions=extensions)

    #   write the paths in txt file
    f = open(filename, 'w')
    count = 1
    for item in paths:
        f.write(f'{str(count)}**{item}')
        f.write('\n')
        count = count + 1

    f.close()

#   