# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import random

get_url = "http://localhost:7200/repositories/refine"

def build_query_origin(parameter: str) -> str:
    interogare = '?subject :hasOrigin <http://example.com/base/{value}>'.format(value=parameter)
    return interogare

def get_from_db(param):
    interogare ="PREFIX : <http://exemplu.ro#> select ?subject where{{ {value} }}".format(value=build_query_origin(parameter=param))
    parameters ={'query': interogare}
    result = requests.get(url=get_url,params=parameters)
    result= result.text.split('\n')
    output = []
    for x in result:
        if len(x.split('#'))>1:
            output.append(x.split('#')[1].replace('\r',''))
    
    return output

class ActionRecommendCar(Action):

    def name(self) -> Text:
        return "action_recommend_car"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        origin = str(tracker.get_slot('car_origin')).split(' ')[-1]
        response = get_from_db(origin)

        dispatcher.utter_message(text="i suggest you get the "+str(random.choice(response)))

        return 
