'''
Decision Tree Classifier
@author: Arpit Vora (ajv9905)
@date: 21 October 2017
'''
import csv
data_input=[];temp=[];output_str='';classifier=[];target_class=[]
class Decitree:
	def read_csv(self,file_name):
		data_input.clear();temp.clear()
		with open(file_name, 'r' ) as f:
			reader = csv.reader(f,delimiter=',');i=0
			for row in reader:
				temp.insert(i,row);i=i+1
		for i in range(0,len(temp)-1):
			data_input.insert(i,temp[i+1])
	def classify(self,data):
		target_class.clear()
		for value in range(0,len(data)):
			if float(data[value][4]) <= 2.85:
				if float(data[value][2]) <= 8.16:
					if float(data[value][3]) <= -0.03:
						 target_class.append('Greyhound')
					else: 
						if float(data[value][3]) <= -0.17:
							 target_class.append('Whippet')
						else: 
							if float(data[value][5]) <= 2.89:
								if float(data[value][3]) <= 2.15:
									 target_class.append('Greyhound')
								else: 
									 target_class.append('Whippet')
							else: 
								if float(data[value][3]) <= 3.17:
									 target_class.append('Whippet')
								else: 
									 target_class.append('Greyhound')
				else: 
					 target_class.append('Greyhound')
			else: 
				if float(data[value][3]) <= 3.99:
					if float(data[value][5]) <= 4.18:
						 target_class.append('Greyhound')
					else: 
						if float(data[value][3]) <= 3.12:
							 target_class.append('Whippet')
						else: 
							 target_class.append('Greyhound')
				else: 
					if float(data[value][5]) <= 4.13:
						 target_class.append('Whippet')
					else: 
						 target_class.append('Greyhound')
			
	def cal_accuracy(self):
		count=0
		for i in range(1,len(temp)):
			if target_class[i-1]==temp[i][6]:
				count+=1
		print('Accuracy for Training Data = ',(count/(len(temp)-1))*100,'%')
	def write_file(self):
		target_class_binary=[]
		for i in range(0, len(temp)):
			if i == 0:
				temp[0].append("Class")
			else:
				temp[i].append(str(target_class[i - 1]))
		with open('HW_05_Vora_Arpit_Classifier_Full_Data.csv', 'w',newline='') as f:
			writer = csv.writer(f);writer.writerows(temp)
		for class_values in target_class:
			if class_values == 'Greyhound':
				target_class_binary.append('1')
			else:
				target_class_binary.append('0')
		with open('HW_05_Vora_Arpit_MyClassifications.csv', 'w',newline='') as fb:
			writer = csv.writer(fb);writer.writerows((target_class_binary))
		print('The final classifier: Greyhound=1 Whippet=0');print(target_class_binary)
def main():
	d= Decitree()
	# uses training data and calculates accuracy for the same
	d.read_csv('HW_05C_DecTree_TRAINING__v540.csv');d.classify(data_input);d.cal_accuracy()
	# uses Testing data and writes the target_class into csv file and also prints the binary representation of class
	d.read_csv('HW_05C_DecTree_TESTING__FOR_STUDENTS__v540.csv');d.classify(data_input);d.write_file()
if __name__ == '__main__':
	main()