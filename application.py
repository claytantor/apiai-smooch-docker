import smooch
import robot
import os
import sys
import json

from flask import Flask, request, g, Response
from werkzeug.local import LocalProxy

app = Flask(__name__)
app.config.from_envvar('FLASK_APPLICATION_SETTINGS')

def get_robot():
    robot_instace = getattr(g, '_robot', None)
    if robot_instace is None:
        robot_instace = g._robot = AIRobotClient(config=app.config, token=app.config['API_AI_TOKEN'])

    return robot_instace

def get_smooch_api():
    smooch_api_instance = getattr(g, '_smooch_api', None)
    if smooch_api_instance is None:

        jwt = smooch.get_jwt(app.config["SMOOCH_KEY_ID"], app.config['SMOOCH_SECRET'])
        smooch_api_instance = g._smooch_api = smooch.SmoochV1(jwt=jwt)

        #test if there are any webhooks for this config
        webhooks_available = smooch_api_instance.list_webhooks()

        #check if the endpoint is in the config
        found = False
        for hook in webhooks_available['webhooks']:
            if hook['target']==app.config["SMOOCH_WEBOOK_ENDPOINT"]:
                found=True

        # tell smooch to start sending events to this place
        if not found:
            smooch_api_instance.save_webhook(app.config["SMOOCH_WEBOOK_ENDPOINT"], ["message:appUser", "postback"])

    return smooch_api_instance

# ========== init app ===========
@app.before_first_request
def init_smooch():
    jwt = smooch.get_jwt(app.config["SMOOCH_KEY_ID"], app.config['SMOOCH_SECRET'])
    smooch_api_instance = smooch.SmoochV1(jwt=jwt)

    #test if there are any webhooks for this config
    webhooks_available = smooch_api_instance.list_webhooks()

    #check if the endpoint is in the config
    found = False
    for hook in webhooks_available['webhooks']:
        if hook['target']==app.config["SMOOCH_WEBOOK_ENDPOINT"]:
            found=True

    # tell smooch to start sending events to this place
    if not found:
        print "creating webhook: {0}".format(app.config["SMOOCH_WEBOOK_ENDPOINT"])
        create_response = smooch_api_instance.save_webhook(app.config["SMOOCH_WEBOOK_ENDPOINT"], ["message:appUser", "postback"])

        print create_response

# ========== routes =============
@app.route("/hc")
def hc():
    """
    health check if you need that.
    """
    data = {'message':'succeed'}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/smooch/events', methods=['POST'])
def smooch_events():
    """
    the firehose of events that the webhooks subscribed to,
    this will send all messages from people who visit your website
    to this endmpoint, the robot then parses those messages and
    does a postback of its response.
    """
    # this is actually everything people say to the robot, may be good
    # to send this to a log file or database
    # print json.dumps(request.json)

    # get the singletons
    smooch_api = LocalProxy(get_smooch_api)
    robot = LocalProxy(get_robot)

    for message in request.json['messages']:
        response = robot.query(line)
        if 'status' in response and response['status']['errorType'] == 'success' and 'result' in response and 'fulfillment' in response['result'] and 'speech' in response['result']['fulfillment']:
            smooch_api.postback_message(response['result']['fulfillment']['speech'], message['authorId'])

    data = {'message':'succeed'}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

def main(argv):
    app.run(host='0.0.0.0', port=int(argv[0]), debug=False)

if __name__ == "__main__":
    main(sys.argv[1:])
