#Setting path variables
import sys
from configs import PROJECT_PATH
sys.path.append(PROJECT_PATH)
#Importing required libraries
import pandas as pd
from Input_Preprocessing import utils
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

#Defining the main class
class recommendationGenerator :

    #Attributes
    userID = 0
    N = 0

    def __init__(self,userID,N):
        self.userID = userID
        self.N = N

    def change_attributes(self,userID,N):
        self.userID = userID
        self.N = N

    def load_data(self,datapath):
        '''
        Loads the required data into pandas.DataFrames to generate the recommendations\n
        Parameters:
            datapath: str  
                Absolute or relative path to the csv file containing the complete data
        Returns:
            1-features dataframe which contains the feature matrix
            2-data dataframe which contains the corresponding (courseID,userID) tuple
        '''

        #Loading the features and converting their type from object to numeric
        features = utils.reduce_mem_usage(pd.read_csv(datapath, usecols = ['click_courseware','load_video','pause_video','problem_check','problem_get','seek_video','stop_video']))
        features = features.apply(pd.to_numeric, errors='coerce')
        features = features.fillna(0)

        #Loading courseID and userID data and converting userID from type object to numeric
        data = pd.read_csv(datapath, usecols = ['courseID','userID'])
        cols = data.columns.drop('courseID')
        data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')
        data = data.fillna(0)

        

        return features, data

    def generate_recommendations(self,features,data, print_rec = False):
        '''
        Generates and prints the recommendations taking the userID and N (the number of recommendations to be generated)\n
        Parameters:
            features: pd.DataFrame
                The features dataframe obtained from the function load_data
            data: pd.DataFrame
                The data dataframe obtained from the function load_data
            print_rec: bool, default False 
                If true, the recommendations are printed. If false, the recommendations are stored in a list
        Returns:
            If print_rec = False, the function returns an ordered list of recommendations
        '''
        index = data[data['userID'] == self.userID].index.tolist()

        #Storig the rows into a new dataframe
        X = features.iloc[index]
        #print(X.shape)
        #print(features.shape)
        
        #Applying cosine similarity and storing the matrix
        cossim_mat = cosine_similarity(X = X.to_numpy(copy = True),Y =features.to_numpy(copy = True),  dense_output= False)

        #Get top N recommendations
        recomm_indices = self.largest_indices(cossim_mat,self.N,data)

        if (print_rec == True):
            #Print the recommendations from the obtained recomm_indices
            self.print_recommendations(recomm_indices,data)
            
            return

        else:
            #Return the list of recommendations
            recomm = []
            i = 0
            for x in data['courseID'][recomm_indices].unique():
                i+=1
                recomm.append(x)
                if(i==self.N):
                    break
            
            return recomm

    def print_recommendations(self,recomm_indices,data):
        '''
        Prints out the unique courses from the obtained recommnded indices.\n
        Parameters:
            recomm_indices: list 
                The list of recommendation indices generated from the function generate_recommendation()
            data: pd.DataFrame 
                The data dataframe obtained from the function load_data()
        '''
        i = 0

        print("Based on the courses {} has previously done".format(self.userID))
        
        for x in data['courseID'][recomm_indices].unique():
            i+=1
            print("Recommendation #{} : {}".format(i,x))
            if(i==self.N):
                break

    '''Utility Methods'''
    def largest_indices(self,ary, top_N, data ):
        """
        Returns the n largest indices from a numpy array.\n
        Parameters:\n
            ary: numpy array 
            top_N: int 
                The number of largest indices to return
            data: pd.DataFrame
                The data dataframe obtained from the function load_data()
        """
        #Flatten the array, find the indices of the top N values then sort the values in a decreasing order
        
        flat = ary.flatten()
        indices = np.argpartition(flat, -top_N)[-top_N:]
        indices = indices[np.argsort(-flat[indices])]
        indices = indices % ary.shape[1]

        '''
        There might be some repeated recommendations and hence the total recommendation might not be equal to N
        Hence we call the function in a recursive manner until the no. of unique recommendations = N
        '''
        n = data['courseID'][indices].unique().shape[0]
        #print(n)
        if (n < self.N):
            indices = self.largest_indices(ary,top_N + (top_N-n),data)

        #Performing MOD by the orignal size as we initially flattened the array
        indices = indices % ary.shape[1]
            
        return indices
     
            

    #def done_courses(self)
