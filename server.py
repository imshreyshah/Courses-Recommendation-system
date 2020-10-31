#Setting path variables
import sys
from configs import *
sys.path.append(PROJECT_PATH)

#Importing required libraries
from flask import Flask,render_template,request
from Recommendation_Generator.generator import recommendationGenerator

features,data = recommendationGenerator.load_data(recommendationGenerator, datapath= DATA_PATH)
users = data['userID'].unique()

app = Flask(__name__)

#HomePage
@app.route("/")
def home():
  return render_template("index.html",max = users.shape[0] -1)

#ResultPage  
@app.route("/result", methods=["GET", "POST"])
def result():
  if request.method == "POST":
    
    #Collecting the form responses
    userdata = request.form

    #Extracting the values for UserIndex and No. of recommendations
    user = int(userdata.get("index"))
    N = int(userdata.get("N"))

    #Getting the userID from the user Index
    users = data['userID'].unique()
    userID = int(users[user])

    #Running the model, generating recommendations and passing the list to the HTML page
    model = recommendationGenerator(userID, N)
    recomm = model.generate_recommendations(features,data)

    return render_template("result.html",userID = userID ,rec_list= recomm)
  
  else:
    
    return "Sorry, there was an error."

if __name__ == "__main__":
  app.run(debug= True)
