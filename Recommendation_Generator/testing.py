'''This file is to test the generator.py file'''

#Setting path variables
import sys
from configs import PROJECT_PATH
sys.path.append(PROJECT_PATH)

from Recommendation_Generator.generator import recommendationGenerator
import pandas as pd
import numpy as np

temp = pd.read_csv('data/final.csv', usecols = ['courseID','userID'])

users = temp['userID'].unique()

print("We have {} unique users in our database".format(users.shape[0]))

print("\n Please enter an index from {} to {} to select a UserID".format(0,users.shape[0] - 1))

user = int(input())
userID = users[user]
print("\n You have selected the user with userID:{} ".format(userID))

print("\nNote that we have total {} number of courses in our database".format(temp['courseID'].unique().shape[0]))
print("\n Please enter the number of recommendations you want. Enter a number between {} - {}".format(1,temp['courseID'].unique().shape[0]))

N = int(input())

print("\n\n")
print("Now lets see the recommendations you have based on your study patterns")

model = recommendationGenerator(userID,N)

features, data = model.load_data(datapath = 'data/final.csv')

model.generate_recommendations(features,data,print_rec = True)
#print(np.shape(list))