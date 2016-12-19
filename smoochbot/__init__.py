import random
import json
import ast
import collections
from fuzzywuzzy import fuzz

def load_robot(filename, robotname):

    robot_config = []
    with open(filename) as json_data:
        robot_config = json.load(json_data)

    for bot in robot_config['bots']:
        if bot['name']==robotname:
            return bot

    return None

class Robot:

    def __init__(self, botdata=None):
        self.bot=botdata

    def get_any_action(self, actionlist):
        index = random.randint(0, len(actionlist)-1)
        return actionlist[index]

    def get_intent(self, id, intents):
        for intent in intents:
            if intent['id']==id:
                return intent
        return None

    def match_phrase(self, lineinput, phrases):
        scores = []
        phrasemap = {}
        for phrase in phrases:
            phrasemap[phrase['id']] = phrase
            for part in phrase['parts']:
                pscore={}
                pscore['part']=part
                pscore['id']=phrase['id']
                pscore['score'] = fuzz.ratio(part, lineinput)
                scores.append(pscore)

        maxscore = max(scores, key=lambda x: x['score'])
        # print scores
        # print maxscore
        return phrasemap[maxscore['id']]

    def convert(self, data):
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(self.convert, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(self.convert, data))
        else:
            return data

    def action_query(self,action,wordmap):
        return action['query'].format(**wordmap)

    def action_say(self,action,wordmap):
        return action['say'].format(**wordmap)

    def process_input(self, lineinput):

        # use the best match to get the intent
        bestphrase = self.match_phrase(lineinput, self.bot['phrases'])

        intent = self.get_intent(bestphrase['intent'], self.bot['intents'])
        # print intent

        if intent['scope']=='any':
            action = self.get_any_action(intent['actions'])
            if 'say' in action:
                wordmap = {}
                return self.action_say(action,wordmap)

        elif intent['scope']=='all':
            for action in intent['actions']:
                if 'query' in action:
                    wordmap = {}
                    print "query: {0}".format(self.action_query(action,wordmap))
                if 'say' in action:
                    wordmap = {}
                    return self.action_say(action,wordmap)

        return "Whatever. I really dont know what to say."
