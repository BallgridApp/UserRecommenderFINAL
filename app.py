from flask import Flask
import GetRecommendation as GR
import checkTimestamps as CT
import fullReset as FR
import UpdateWeights as UW
import weightUpdateScheduler as US
app = Flask(__name__)
@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"
@app.route('/getRecommendation/<ref>', methods = ['GET'])
def getRecommendation(ref):
    return GR.giveRecommendation(ref)
@app.route('/checkInactiveWeekly', methods = ['POST'])
def checkInactiveWeekly():
    CT.checkInactiveWeekly()
    return 'Status: 200'
@app.route('/checkActiveWeekly', methods = ['POST'])
def checkActiveWeekly():
    CT.checkActiveWeekly()
    return 'Status: 200'
@app.route('/fullReset', methods = ['POST'])
def fullReset():
    FR.fullReset()
    return 'Status: 200'
@app.route('/updateWeights/<ref>', methods = ['POST'])
def updateWeights(ref):
    UW.updateWeights(ref)
    return 'Status: 200'
@app.route('/checkUpdateLogin/<ref>', methods = ['POST'])
def checkUpdateLogin(ref):
    US.checkUpdateLogin(ref)
    return 'Status: 200'
@app.route('/createUser/<ref>', methods = ['POST']) # wont work unless fully created user in Fauna
def createUser(ref):
    UW.createUser(ref)
    return 'Status: 200'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)


#GET: giveRecommendation(UwU),
#POST: Check Inactive Weekly(UwU), Check Active Weekly(UwU), fullReset(UwU), updateWeights(UwU), checkUpdateLogin(UwU), createUser(UwU)
