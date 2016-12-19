#!/usr/bin/env python
# coding: utf-8

import urllib2
import urllib
import json
from urllib2 import HTTPError
import uuid

class AIRobotClient:

    """
    This client hides the implementation
    specifics for the oauth and non oauth versions
    of the application

    curl 'https://api.api.ai/api/query?v=20150910&query=show%20aws%20buckets&lang=en&sessionId=9d5b2070-cc86-4f02-bb03-b693423dba2e&timezone=2016-12-02T21:12:55-0800' -H 'Authorization:Bearer fd42729144eb45d5b287262951ea1359'

    """
    def __init__(self, config, token=None, sessionId=None, lang="en"):
        self.config = config
        self.base_url="https://api.api.ai"
        self.token=token
        self.lang=lang
        if sessionId==None:
            self.sessionId=str(uuid.uuid4()).replace("-", "")[16:]

    def get_json(self, url, data_obj={}, jwt=None):
        try:
            querystring = urllib.urlencode(data_obj)
            url_final = "{0}?{1}".format(url,querystring)
            self.log_debug(url_final)

            get_headers={'Content-Type': 'application/json'}
            if jwt:
                get_headers['Authorization']='Bearer {0}'.format(jwt)
                self.log_debug(get_headers)

            req = urllib2.Request(url_final, headers=get_headers)
            response = urllib2.urlopen(req)
            json_response = response.read()
            return json.loads(json_response)
        except HTTPError as e:
            print e
            return json.loads('{}')

    def post_json(self, url, data_obj={}, jwt=None):
        try:
            data_json = json.dumps(data_obj)
            post_headers={'Content-Type': 'application/json'}
            if jwt:
                post_headers['Authorization']='Bearer {0}'.format(jwt)
            req = urllib2.Request(url, data=data_json, headers=post_headers)
            f = urllib2.urlopen(req)
            val_response = f.read()
            f.close()
            response_obj = json.loads(val_response)
            return response_obj
        except HTTPError as e:
            print e
            return json.loads('{}')

    def add_base_params(self, data):
        data['v'] = '20150910'
        data['lang'] = self.lang
        data['sessionId'] = self.sessionId

    def post(self, call, data={}):
        self.add_base_params(data)

        call_url = "{0}/api/{1}".format(self.base_url,call)
        resp = self.post_json(call_url, data_obj=data, token=self.token)
        return resp

    def get(self, call, data={}):
        self.add_base_params(data)

        call_url = "{0}/api/{1}".format(self.base_url,call)
        resp = self.get_json(url=call_url, data_obj=data, jwt=self.token)
        return resp

    def query(self, message):
        url="query"
        req = { 'query':message.rstrip() }
        response = self.get(url, req )
        self.log_debug("response: {0}".format(json.dumps(response, indent=4)))
        return response

    def log_debug(self, message):
        if 'DEBUG' in self.config and self.config['DEBUG']=="True":
            print message
