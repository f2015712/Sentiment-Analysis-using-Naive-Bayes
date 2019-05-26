import sys
import re
import random

"""This method is used to split the data into training and testing dataset.
It takes 2 parameters i.e a 2D array containing sentences along with their labels and factor which is the split factor.
The split factor tells in what ratio we need to divide the testing and training data. It returns 2 arrays, i.e a Training and a Testing 
dataset."""

def Split_Data(sentiments,factor):
    split_factor = factor
    Sample_Data = [i for i in range(len(sentiments))]
    #Using random function, we select random data from sentiments array to add to training data.
    Training = random.sample(range(0, len(sentiments)), int(split_factor * len(sentiments)))

    Training = list(set(Training))
    Testing = list(set(Sample_Data).difference(Training)) #This makes sure that Training and testing data are mutually exclusive.

    Testing_Data = []
    Training_Data = []
    for i in range(len(Training)):
        Training_Data.append(sentiments[Training[i]])
    for i in range(len(Testing)):
        Testing_Data.append(sentiments[Testing[i]])
    return Training_Data, Testing_Data

"""This method is used to calculate Accuracy, Precision, Recall and F1 Score.
It takes  4 inputs i.e frequency of True Positives,True Negatives, False Positives and False Negatives."""

def Calculate_Score(True_Positive,True_Negative,False_Positive,False_Negative):
    Accuracy=(float(True_Negative+True_Positive))/(True_Negative+True_Positive+False_Negative+False_Positive)
    Precision=(float(True_Positive))/(True_Positive+False_Positive)
    Recall=(float(True_Positive))/(True_Positive+False_Negative)
    F1_Score=2*(Precision*Recall)/(Precision+Recall)
    print("Accuracy is "+str(Accuracy))
    print("Precision is "+str(Precision))
    print("Recall is "+str(Recall))
    print("F1 Score is "+str(F1_Score))


"""This method is used to get the count of number of words in Positive and Negative sentences respectively."""

def Get_Count(TRAINING_DATA):
    Number_of_Positive = 0
    Number_of_Negatives = 0
    for i in range(len(TRAINING_DATA)):
        if TRAINING_DATA[i][0] == 'pos':# If the label is positive,get the count of number of words in that sentence.
            Number_of_Positive += (len(TRAINING_DATA[i]) - 1)
        else:
            Number_of_Negatives += (len(TRAINING_DATA[i]) - 1) #If label is negative, store count of number of words in that sentence.
    return Number_of_Positive,Number_of_Negatives

"""This method is used to generate the confusion matrix for the Testing Data. 
It takes Testing Data which is a 2D array as input and returns the values of the cells in
a confusion matrix"""

def Confusion_Matrix(TESTING_DATA):
    True_Positive = 0
    True_Negative = 0
    False_Positive = 0
    False_Negative = 0

    for x in range(len(TESTING_DATA)):

        words = TESTING_DATA[x]
        POS = 1
        NEG = 1
        POSITIVE_OCCURENCES = 0
        NEGATIVE_OCCURENCES = 0
        for i in range(1, len(words)):
            if words[i] in positive_words:
                POSITIVE_OCCURENCES = positive_words[(words[i]).lower()]
                if POSITIVE_OCCURENCES<=50: #Don't consider a word if its occuring less than or equal to 50 times.
                    continue
            if words[i] in negative_words:
                NEGATIVE_OCCURENCES = negative_words[(words[i]).lower()]
                if NEGATIVE_OCCURENCES<=50: #Don't consider a word if its occuring less than or equal to 50 times.
                    continue

            POS *= (float(POSITIVE_OCCURENCES + 1)) / (len(bag_of_words) + Number_of_Positive)
            NEG *= (float(NEGATIVE_OCCURENCES + 1)) / (len(bag_of_words) + Number_of_Negatives)


        POS=pos*POS #POS multiplied by the probability of positive i.e pos
        NEG=neg*NEG #NEG multiplied by the probability of negative i.e neg

        if (POS>NEG):
            Predicted = 'pos'
        else:
            Predicted = 'neg'


        Actual = words[0] #The first word gives the label i.e positive or negative
        if Predicted == 'pos' and Actual == 'pos':
            True_Positive += 1
        elif Predicted == 'pos' and Actual == 'neg':
            False_Positive += 1
        elif Predicted == 'neg' and Actual == 'pos':
            False_Negative += 1
        elif Predicted == 'neg' and Actual == 'neg':
            True_Negative += 1
    print("True Positives = "+str(True_Positive))
    print("True Negatives = "+str(True_Negative))
    print("False Positives = "+str(False_Positive))
    print("False Negatives = "+str(False_Negative))
    Calculate_Score(True_Positive,True_Negative,False_Positive,False_Negative)

"""This method id used to get the data from a text file and store it into a 2D array. It also counts 
the number of positive and negative examples. Also, we have a dictionary named bag_of_words for storing 
all the unique words present in the document."""

def Get_Input(path):

    delimeter = ",|-| |;|\.|\(|\)|\n|\"|:|'|/|&|`|[|]|\{|\}"
    bag_of_words = {}
    negative_words = {}
    positive_words = {}
    sentiments = []
    pos = 0
    neg = 0
    with open(path, encoding="utf8") as f:

        for line in f:

            words = re.split(delimeter, line) #Split a sentence into array of words

            if words[1] == 'neg':
                neg += 1 #Counting number of negative examples
                for i in range(4, len(words)):
                    if words[i] not in negative_words:
                        negative_words[words[i]] = 1
                    else:
                        negative_words[words[i]] += 1
            elif words[1] == 'pos':
                pos += 1#Counting number f positive examples
                for i in range(4, len(words)):
                    if words[i] not in positive_words:
                        positive_words[words[i]] = 1
                    else:
                        positive_words[words[i]] += 1

            temp = [words[1]]  # Storing sentences along with their labels
            for i in range(4, len(words)):
                if len(words[i]) != 0:
                    temp += [(words[i]).lower()]

            sentiments.append(temp)



            for i in range(4): #Removing file name, format, and label.
                words.pop(0)

            for i in range(len(words)):

                if len(words[i]) != 0:
                    bag_of_words[(words[i]).lower()] = 1 #Putting words in bag_of_words. It contains the number of unique words in the doc.
    POSITIVE_WORDS={}
    for i in positive_words:
        if positive_words[i]<=10: #Remove less frequent words
            continue
        else:
            POSITIVE_WORDS[i]=positive_words[i]
    NEGATIVE_WORDS={}
    for i in negative_words:
        if negative_words[i]<=10: #Remove less frequent words
            continue
        else:
            NEGATIVE_WORDS[i]=negative_words[i]


    return sentiments,POSITIVE_WORDS,NEGATIVE_WORDS,bag_of_words,pos,neg


#Read and store necessary information from the text file given as input data.
sentiments,positive_words,negative_words,bag_of_words,pos,neg = Get_Input('naive_bayes_data.txt')

#Split the 2D array data i.e sentiments array into 2 sets i.e training and testing data and specify the split_factor
TRAINING_DATA, TESTING_DATA = Split_Data(sentiments,0.8)
#Get the count of number of positive and negative words
Number_of_Positive,Number_of_Negatives=Get_Count(TRAINING_DATA)
#Generate the confusion matrix
Confusion_Matrix(TESTING_DATA)


