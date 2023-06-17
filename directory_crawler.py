import os

#   custom implementation of a directory crawler, I could have
#   used the one provided by the pyhthon library but I wanted
#   to waste time instead lmao.
def getFiles(path, extensions) -> tuple[list, list, int]:
    
    #   replace path delimiters
	path  = path.replace('/', '\\')
	
    #   get all files and directories in root directory
	files = os.listdir(path)
	
	count = 0
	
	folderStack = list()
	foundStack = list()
	
	#	ADD ROOT FOLDER TO THE STACK
	folderStack.append(path)
	foundStack.append(f'{path}')
	
	while len(folderStack)>0:
		files = os.listdir(folderStack[-1])
		currentDir = folderStack[-1]
		folderStack.pop()
		#	GET ALL DIRECTORIES IN ROOT FOLDER
		for file in files:
			if os.path.isdir(f'{currentDir}{file}'):
				folderStack.append(f'{currentDir}{file}\\')
				foundStack.append(f'{currentDir}{file}')
	
	filePathsList = list()
	filesList = list()
	dirsCount = len(foundStack) 
	count = 0
	#extensions  = ['.mp3', '.m4a']

    #	GET ALL FILES IN EACH DIRECTORY IN THE STACK
	for item in foundStack:
		files = os.listdir(f'{item}\\')
		for file in files:
			if os.path.isfile(f'{item}\\{file}'):
				for extension in extensions:
					if file.find(extension)>0:
						count+=1
						filePathsList.append(f'{item}\\{file}')
						filesList.append(f'{file}')

    #   return files, as filenames
    #   return files, in the form of their absolute paths
    #   return number of sub directories in root directory
	return filesList, filePathsList, dirsCount

