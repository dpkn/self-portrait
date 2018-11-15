# A super simple API server that replies with a generated message from textgenrnn
# This is the first time ever I'm attempting to make a python server
# Please do not trust any of this code at all
# If you put this on production bad things will happen
# Visit the server on the /message route to get a textgenrnn message

import flask
from flask_restful import Api, Resource, reqparse
from textgenrnn import textgenrnn

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
def init():
    global chatGen,chatMessage
    chatGen = textgenrnn('./model.hdf5')
    chatMessage = chatGen.generate(n=1, temperature = 1, return_as_list=True)

# API for prediction
@app.route("/message", methods=["GET"])
def predict():
    chatMessage = chatGen.generate(n=1, temperature = 0.7, return_as_list=True)
    return sendResponse({'message': chatMessage[0]})

# Cross origin support
def sendResponse(responseObj):
    response = flask.jsonify(responseObj)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Allow-Headers', 'accept,content-type,Origin,X-Requested-With,Content-Type,access_token,Accept,Authorization,source')
    response.headers.add('Access-Control-Allow-Credentials', True)
    return response

# if this is the main thread of execution first load the model and then start the server
if __name__ == "__main__":
    print(("* Loading model and Flask server..."
        "please wait until server has fully started"))
    init()
    app.run(threaded=True)
