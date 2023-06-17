def to_list(file):
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
			#print(temp)
	return temp_list

def to_list_single(file):
	temp_list = list()
	temp_str = ''

	for f in file:
		if(f!='\n' and f!=' '):
			temp_str += f
			temp_list.append(temp_str.replace('\n', ''))
			temp_str = ''

	return temp_list

