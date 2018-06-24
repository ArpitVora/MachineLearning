"""
This program writes a program (Decision Tree Classifier) for classification 
@author : Arpit Jayesh Vora (ajv9905)
@date : 17 Sept 2017
"""
import csv
import numpy as np
data_input=[]
temp=[];
indent=""
output_str=''
classifier=[]
class Decitree:
    """
    This class reads input file, calculates best attribute and best value using Impurity factor as Gini Index
    Then it checks for the stopping criteria, if not satisfied then splits data based on the best attribute
    and then recursively calls left part and write part.
    Output is the classifier file generated
    """
    def read_csv(self):
        """
        This method reads the data and saves into the data structure for calculations
        """
        with open('HW_05C_DecTree_TRAINING__v540.csv', 'r' ) as f:
            reader = csv.reader(f,delimiter=',')
            i=0
            for row in reader:
                temp.insert(i,row)
                i=i+1;
        # data_input is the data without header
        for i in range(0,len(temp)-1):
            data_input.insert(i,temp[i+1])

    def calGini(self,data,data_temp,temp_thr):
        """
        This method calculates the Gini index for all values of all attributes
        :param data: Its the entire set of the data
        :param data_temp: It is the data for a particular attribute
        :param temp_thr: it is the threshold value, ie all values considered
        :return: returns the best_gini Index
        """
        countForGrehound0 = 0;
        countForGrehound1 = 0;
        countForWhippet0 = 0;
        countForWhippet1 = 0
        for value in range(0, len(data_temp)):
            if float(data_temp[value]) <= float(temp_thr):
                if data[value][6] == 'Greyhound':
                    countForGrehound0 += 1;
                else:
                    countForWhippet0 += 1
            else:
                if data[value][6] == 'Greyhound':
                    countForGrehound1 += 1;
                else:
                    countForWhippet1 += 1
        if countForGrehound0 + countForWhippet0 != 0:
            prob1 = float(countForGrehound0) / float(countForGrehound0 + countForWhippet0);
            prob2 = float(countForWhippet0) / float(countForGrehound0 + countForWhippet0)
            gini1 = 1 - (prob1 * prob1) - (prob2 * prob2)
        else:
            gini1 = 0
        if countForGrehound1 + countForWhippet1 != 0:
            prob3 = float(countForGrehound1) / float(countForGrehound1 + countForWhippet1)
            prob4 = float(countForWhippet1) / float(countForGrehound1 + countForWhippet1)
            gini2 = 1 - (prob3 * prob3) - (prob4 * prob4)
        else:
            gini2 = 0
        wt_gini = ((gini1 * ((countForWhippet0 + countForGrehound0) / (len(data_temp)))) + (gini2 * ((countForWhippet1 + countForGrehound1) / (len(data_temp)))))
        return wt_gini

    def calDeciTree(self,data,indent):
        """
        This method is the actual decision tree which generates the classifier, stored in a list classifier
        :param data: The input data for each call, ie. left_data when call recursively
        :param indent: this is used to give proper indentation to the classifier code generated
        :return: It returns the class (Greyhound or Whippet) according to the algorithm conditions
        """
        best_threshold=np.inf;best_attribute=np.inf;best_gini=np.inf;
        for attribute in range(0,len(data[0])-1):
            data_temp=[];column=0;
            for row in range(0,len(data)):
                data_temp.append(data[row][attribute])
            for temp_thr in data_temp:
                column+=1
                wt_gini=self.calGini(data,data_temp,temp_thr)
                if wt_gini<best_gini:
                    best_gini=wt_gini
                    best_threshold=temp_thr
                    best_attribute=attribute
                    best_column=column
        split=0
        data.sort(key=lambda data: data[best_attribute])
        # Stopping Condition
        return_class=self.checkStopCri(data)
        if return_class!= '':
            return return_class
        # if condition not satisfied then split data
        for j in range(0,len(data)):
            if data[j][best_attribute]==best_threshold:
                split=j;
        left=data[0:split];right=data[split+1:len(data)+1]
        output_str=indent+"if float(data[value][" + str(best_attribute) +"]) <= " + best_threshold +":"
        classifier.append(output_str)
        #recursively call left data
        if len(left)!=0:
            left_parse=self.calDeciTree(left,indent+"\t")
            if left_parse is not None:
                output_str=indent+"\t target_class.append('"+left_parse+"')"
                classifier.append(output_str)
        else:
            output_str = indent + "\t target_class.append('" + 'Greyhound' + "')"
            classifier.append(output_str)
        classifier.append(indent+"else: ")
        # recursively call right data
        if len(right)!=0:
            right_parse=self.calDeciTree(right,indent+"\t")
            if right_parse is not None:
                output_str=indent+"\t target_class.append('"+right_parse+"')"
                classifier.append(output_str)
        else:
            output_str = indent + "\t target_class.append('" + 'Whippet' + "')"
            classifier.append(output_str)

    def checkStopCri(self, data_check=[]):
        """
        This method is a helper function for the stopping condition.Here if the data is 100% pure
        we stop further splitting of data and return the class classified
        :param data_check: It is the data for which it checks the condition
        :return: It returns the class (Greyhound/Whippet/Null)
        """
        countGreyhound=0;countWhippet=0;perGreyhound=0;perWhippet=0;
        for values in range(0,len(data_check)):
            if data_check[values][6]=='Greyhound':
                countGreyhound+=1;
            else:
                countWhippet+=1;
        perGreyhound = 0.9*len(data_check)
        perWhippet=0.9*len(data_check)
        if len(data_check)>30:
            if countGreyhound >= perGreyhound:
                return 'Greyhound'
            elif countWhippet >= perWhippet:
                return 'Whippet'
            else:
                return ''
        elif countWhippet==countGreyhound:
            return 'Greyhound'
        else:
            if countGreyhound>countWhippet:
                return 'Greyhound'
            else:
                return 'Whippet'
    def write_file(self):
        """
        This method is used to write the classifier file. It has different parts to write a file
        ie Header, Prologue, Classifier and epilogue.
        """
        with open('HW_05_Vora_Arpit_Classifier.py','w') as f:
            write=["'''\n","HW05 : Decision Tree Classifier\n","@author: Arpit Vora (ajv9905)\n","@date: 21 October 2017\n","@reference : Prof. Dr. Thomas B. Kinsman's notes and python docs for libraries\n","'''\n"]
            prologue=['import csv\n',
                      "data_input=[];temp=[];output_str='';classifier=[];target_class=[]\n",
                      'class Decitree:\n\tdef read_csv(self,file_name):\n\t\t',
                      "data_input.clear();temp.clear()\n\t\t"
                      "with open(file_name, 'r' ) as f:\n\t\t\t",
                      "reader = csv.reader(f,delimiter=',');i=0\n\t\t\t"
                      'for row in reader:\n\t\t\t\ttemp.insert(i,row);i=i+1\n\t\t'
                      'for i in range(0,len(temp)-1):\n\t\t\tdata_input.insert(i,temp[i+1])\n\t'
                      'def classify(self,data):\n\t\ttarget_class.clear()\n\t\tfor value in range(0,len(data)):\n\t\t\t']
            f.writelines(write)
            f.writelines(prologue)
            for i in range(0,len(classifier)):
                f.writelines(classifier[i]+'\n\t\t\t')
            epilogue=["\n\t",
                      "def cal_accuracy(self):\n\t\t",
                      "count=0\n\t\t","for i in range(1,len(temp)):\n\t\t\t",
                      "if target_class[i-1]==temp[i][6]:\n\t\t\t\t",
                      "count+=1\n\t\t","print('Accuracy for Training Data = ',(count/(len(temp)-1))*100,'%')\n\t"
                      "def write_file(self):\n\t\ttarget_class_binary=[]\n\t\tfor i in range(0, len(temp)):\n\t\t\t",
                      'if i == 0:\n\t\t\t\ttemp[0].append("Class")\n\t\t\t',
                      "else:\n\t\t\t\ttemp[i].append(str(target_class[i - 1]))\n\t\t"
                      "with open('HW_05_Vora_Arpit_Classifier_Full_Data.csv', 'w',newline='') as f:\n\t\t\t",
                      "writer = csv.writer(f);writer.writerows(temp)\n\t\t",
                      "for class_values in target_class:\n\t\t\t",
                      "if class_values == 'Greyhound':\n\t\t\t\t",
                      "target_class_binary.append('1')\n\t\t\t",
                      "else:\n\t\t\t\t",
                      "target_class_binary.append('0')\n\t\t",
                      "with open('HW_05_Vora_Arpit_MyClassifications.csv', 'w',newline='') as fb:\n\t\t\t",
                      "writer = csv.writer(fb);writer.writerows((target_class_binary))\n\t\t",
                      "print('The final classifier: Greyhound=1 Whippet=0');print(target_class_binary)\n"]
            f.writelines(epilogue)
            main_method=["def main():\n\t",
                         "d= Decitree()\n\t",
                         "# uses training data and calculates accuracy for the same\n\t",
                         "d.read_csv('HW_05C_DecTree_TRAINING__v540.csv');d.classify(data_input);d.cal_accuracy()\n\t",
                         "# uses Testing data and writes the target_class into csv file and also prints the binary representation of class\n\t",
                         "d.read_csv('HW_05C_DecTree_TESTING__FOR_STUDENTS__v540.csv');d.classify(data_input);d.write_file()\n"
                         "if __name__ == '__main__':\n\tmain()"]
            f.writelines(main_method)
def main():
    """
    This is main method which calls all the methods in class Decitree
    :return:
    """
    d= Decitree()
    d.read_csv()
    d.calDeciTree(data_input,indent)
    d.write_file()
    print('The classifier file is generated')
if __name__ == '__main__':
    main()