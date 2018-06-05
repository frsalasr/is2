def average(number_list):

	if len(number_list) == 0:
		return 0
		
	result = 0
	for number in number_list:
		result = result + number

	return result/len(number_list)