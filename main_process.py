import directory_crawler as dc
import os

#   enumerates the directory, gets files
#   creates txt reprenting files present
#   returns nothing
def getFiles(filename: str, path: str, extensions: set, absPath: str):
    #   get all files in dest dir
    tempFiles, tempPaths, dirsCount = dc.getFiles(path=path, extensions=extensions)

    #   rename all files in dest dir, to remove special unicode, esp emojis smh
    for tempPath in tempPaths:
        pathBytes = tempPath.encode('ascii', 'ignore')
        newPath = pathBytes.decode()
        os.rename(tempPath, newPath)

    #   recompile the dest contents
    files, paths, dirCount = dc.getFiles(path=path, extensions=extensions)

    #   add attributes
    #   get file sizes, use that to determine size of the root directory
    size = 0 
    for cFile in paths:
        size += os.path.getsize(cFile)


    #   write the paths into txt file
    f = open(filename, 'w')
    count = 1
    for item in paths:
        itemName = item.replace(absPath, '')
        f.write(f'{str(count)}**{itemName}')
        f.write('\n')
        count = count + 1

    #   save the root directory attribute incl. size, file count
    #   and directory count
    #   append at end of txt file
    f.write(f'files##{len(paths)}')
    f.write('\n')
    f.write(f'dirs##{(dirCount)}')
    f.write('\n')
    f.write(f'size##{(size)}')
    
    f.close()
