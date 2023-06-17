#   this takes a file descriptor and returns 
#   the contents of a txt as a list
def to_list(file) -> list:
	counter = 0 
	temp_list = list()
	temp_str = ''

	for f in file:
		if(f!='\n'):
			temp = f
			if(counter<=9):
				temp_str = temp[0] + temp[1]
			elif(counter>9):
				temp_str = temp[0] + temp[1]+ temp[2]
			temp_list.append(temp_str)
			temp_str = ''
			counter+=1
			
	return temp_list

#   returns all contents of txt in a single list
def to_list_single(file) -> list:
	temp_list = list()
	temp_str = ''

	for f in file:
		if(f!='\n' and f!=' '):
			temp_str += f
			temp_list.append(temp_str.replace('\n', ''))
			temp_str = ''

	return temp_list

