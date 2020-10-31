# Course Recommendation Engine based on online Study patterns

## Project Description
The project aims to recommend courses to students based on their study patterns and cognitive level. It was built as a part of my internship at [SilverTouch Technologies LTD](https://www.silvertouch.com/).

Trivially recommendations are made based on course ratings which leads to only highly rated courses being recommended. This approach ignores the fact that the cognitive level of the student might not be suitable for those courses.

Hence this recommendation engine takes the user activity of a user in courses he/she has already finished. Then it finds similar users who had shown similar patterns in activities in other courses.
Now those courses shall be recommended to the user where he/she shall be expected to complete the course as the course difficulty level matches his/her cognitive level.

This approach is a type of collaborative filtering approach to generate recommendations.

## Model Description
The model takes the online activity of a student as input in the form of log files. 
As a part of the first step, I built the **Input processing module** which converts the huge log files to usable feature matrix in two steps. 
Next, the model takes those features and compares the cosine pairwise similarity with other users and finds similar users. 
Finally the model outputs an ordered list of top N recommendations. 
The model has been presented as a simple API built using the Flask framework. 

## How to run the app
First you need to set the system path. You can do that by setting the project path in configs.py file

Now, while being in the directory containing server.py file type the following command:

`python3 server.py`

You will get a prompt to open your localhost where you can try out generating recommendations.

The app asks for an index value to randomly pick up an userID from the database. It asks for the number of recommendations to be generated as well. 
(The number is set between 1-100 based on the dataset size).

## Dataset used
The orignal dataset contained raw log files of uder activities. The orignal dataset can be found at http://moocdata.cn/data/user-activity.
I have added a sample of converted dataset which essentially is a feature matrix containing pairs of userID and courseID along with the frequency of different activities that the user performed in that course.

## Description of folders/modules

### Data
It contains the sample data to be used.

### Input Preprocessing 
The preprocessing.py module contains functions used for converting the initial log files to usable CSV files in usable form. 
Next it has the function to convert the raw data containing CSV file to feature matrix which is used by the model.

## Recommendation_Generator
The generator.py file contains the main model that generates the recommendation list.

## Author
Shrey Shah [GitHub](https://github.com/imshreyshah) [LinkedIn](https://www.linkedin.com/in/imshreyshah/)
  