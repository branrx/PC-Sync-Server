import os

def getFilesAndDirs(path, extensions):
	#path = 'D:\\test space\\'
	path  = path.replace('/', '\\')
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
	directories = list()
	
	count = 0 
	#extensions  = ['.mp3', '.m4a']
	for item in foundStack:
		files = os.listdir(f'{item}\\')
		for file in files:
			if os.path.isfile(f'{item}\\{file}'):
				for extension in extensions:
					if file.find(extension)>0:
						count+=1
						filePathsList.append(f'{item}\\{file}')
						filesList.append(f'{file}')
			else:
				if f'{item}\\{file}' not in directories:
					directories.append(f'{item}\\{file}')

	return filesList, filePathsList, directories


def getFiles(path, extensions):
	#path = 'D:\\test space\\'
	path  = path.replace('/', '\\')
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
	for item in foundStack:
		files = os.listdir(f'{item}\\')
		for file in files:
			if os.path.isfile(f'{item}\\{file}'):
				for extension in extensions:
					if file.find(extension)>0:
						count+=1
						filePathsList.append(f'{item}\\{file}')
						filesList.append(f'{file}')


	return filesList, filePathsList, dirsCount

