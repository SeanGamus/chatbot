import json
import requests
import random
from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

citypin = '600040'
catalog = 'Free Food'


class ActionSearch(Action):

    def name(self):
        return "srch"

    def run(self, dispatcher, tracker, domain):

        citypin = tracker.get_slot('pin_code')
        catalog = tracker.get_slot('category')
        if len(citypin) == 6:
            print(citypin)
            url = "https://api.postalpincode.in/pincode/" + citypin
            response = requests.get(url)
            data = response.json()
            city_name = data[0]['PostOffice'][0]['District']

            url = "http://ec2-3-23-130-174.us-east-2.compute.amazonaws.com:8000/resource? city=" + \
                city_name + "&category=" + catalog
            response = requests.get(url)
            data = response.json()
            r_info = data['data'][0]
            cat = r_info['category']
            desc = r_info['description']
            org = r_info['organisation']
            pno = r_info['phone']
            dispatcher.utter_message(
                text=f"Category: {cat}\n Description: {desc}\n Organisation: {org}\n Contact Info: {pno}\n")
        else:
            dispatcher.utter_message("Enter Valid Pincode")
        return[]


class ActionNeedHelp(Action):
    def name(self):
        return "need_help"

    def run(self, dispatcher, tracker, domain):
        citypin = tracker.get_slot('pin_code')
        dispatcher.utter_message(
            text=f"Do you want to get the resources for - {citypin}. Press YES to confirm and NO to change another pincode")
        return[]


class ActionCategoryNeeded(Action):
    def name(self):
        return "categorise"

    def run(self, dispatcher, tracker, domain):
        catalog = tracker.get_slot('category')
        dispatcher.utter_message(
            text=f"Do you want to get {catalog} . Press YES to confirm and NO to change ")

        return[]


class ActionCategories(Action):
    def name(self):
        return "category_u"

    def run(self, dispatcher, tracker, domain):

        response = requests.get(
            "http://ec2-3-23-130-174.us-east-2.compute.amazonaws.com:8000/categories")
        data = response.json()

        dispatcher.utter_message(
            text=f"Please select from the Categories given below:\n{data['data']}")

        return[]
