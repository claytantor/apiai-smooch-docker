import urllib2
import json
from urllib2 import HTTPError
import urlparse
import jwt

def get_jwt(key, secret):
    encoded_jwt = jwt.encode({'scope': 'app'}, secret, algorithm='HS256', headers={'kid': key})
    return encoded_jwt

class SmoochV1():

    def __init__(self, jwt=None, base_url="https://api.smooch.io"):
        self.base_url=base_url
        self.jwt=jwt

    def get_json(self, url, jwt=None):
        try:
            req = urllib2.Request(url, headers={'Content-Type': 'application/json', 'Authorization':'Bearer {0}'.format(jwt)})
            response = urllib2.urlopen(req)
            json_response = response.read()
            return json.loads(json_response)
        except HTTPError as e:
            print e
            return json.loads('{}')

    def post_json(self, url, data_obj={}, jwt=None):
        try:
            data_json = json.dumps(data_obj)
            req = urllib2.Request(url, data=data_json, headers={'Content-Type': 'application/json', 'Authorization':'Bearer {0}'.format(jwt)})
            f = urllib2.urlopen(req)
            val_response = f.read()
            f.close()
            response_obj = json.loads(val_response)
            return response_obj
        except HTTPError as e:
            print e
            return json.loads('{}')

    def put_json(self, data_obj={}, jwt=None):
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(url, data=data_obj, headers={'Content-Type': 'application/json','Authorization':'Bearer {0}'.format(jwt)})
            request.get_method = lambda: 'PUT'
            url = opener.open(request)
        except HTTPError as e:
            print e
            return json.loads('{}')

    def del_json(self, url, jwt=None):
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(url, headers={'Content-Type': 'application/json', 'Authorization':'Bearer {0}'.format(jwt)})
            request.get_method = lambda: 'DEL'
            url = opener.open(request)
        except HTTPError as e:
            print e
            return json.loads('{}')

    def save_webhook(self, subscriber_url, triggers):
        # POST /v1/webhooks
        # {"target": "https://robot.yourdomain.com/smooch/events", "triggers":["message:appUser", "postback"]}

        req = {}
        req['target'] = subscriber_url
        req['triggers'] = triggers
        resp = self.post_json("{0}/v1/webhooks".format(self.base_url), data_obj=req, jwt=self.jwt)

        # {
        #   "webhook": {
        #     "target": "https://robot.yourdomain.com/smooch/events",
        #     "secret": "ae8b6e264fe492466b4ce044e6a262f46ccd3387",
        #     "_id": "58371406d99770700071daf0",
        #     "triggers": [
        #       "message:appUser",
        #       "postback"
        #     ]
        #   }
        # }
        return resp


    def list_webhooks(self):
        #GET /v1/webhooks
        resp = self.get_json("{0}/v1/webhooks".format(self.base_url), jwt=self.jwt)

        # {
        #   "webhooks": [
        #     {
        #       "target": "https://robot.yourdomain.com/smooch/events",
        #       "secret": "ae8b6e264fe492466b4ce044e6a262f46ccd3387",
        #       "_id": "58371406d99770700071daf0",
        #       "triggers": [
        #         "message:appUser",
        #         "postback"
        #       ]
        #     }
        #   ]
        # }
        return resp

    def delete_webhook(self, id):
        # DEL /v1/webhooks
        resp = self.del_json("{0}/v1/webhooks/{1}".format(self.base_url,id),jwt=self.jwt)
        # 200 status code
        return resp

    def postback_message(self, message, userId, role="appMaker"):
        # POST /v1/appusers/[userId to post to]/messages
        # {"text":"Just put some vinegar on it", "role": "appMaker"}

        req = {}
        req['text'] = message
        req['role'] = role
        resp = self.post_json("{0}/v1/appusers/{1}/messages".format(self.base_url, userId), data_obj=req, jwt=self.jwt)

    def find_client_id(self, all_clients, client_endpoint):

        # only send to wensite client
        for client in all_clients:
            if client['info']['currentUrl'] == client_endpoint:
                return client['id']

        return None
