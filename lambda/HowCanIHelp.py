from __future__ import print_function

import boto3
import json

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    #print (event);
    if (event["session"]["application"]["applicationId"] !=
            "[your_application_id]"):
        raise ValueError("Invalid Application ID")

    if (event["session"]["new"]):
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if (event["request"]["type"] == "LaunchRequest"):
        return on_launch(event["request"], event["session"])
    elif (event["request"]["type"] == "IntentRequest"):
        return on_intent(event["request"], event["session"])
    elif (event["request"]["type"] == "SessionEndedRequest"):
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print ("Starting new session.")

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    slots = intent_request["intent"]["slots"]

    if (intent_name == "GetCategories"):
        return get_categories()
    elif (intent_name == "GetEventsByCategory"):
        category = slots["Category"]["value"].title()
        return get_events_by_category(category)
    elif (intent_name == "GetEventsByDate"):
        return get_events_by_date()
    elif (intent_name == "GetMyEvents"):
        return get_my_events()
    elif (intent_name == "GetEventsNearMe"):
        return get_events_near_me(intent)
    elif (intent_name == "AMAZON.HelpIntent"):
        return get_welcome_response()
    elif (intent_name == "AMAZON.CancelIntent") or (intent_name == "AMAZON.StopIntent"):
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print ("Ending session.")
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "How Can I Help?"
    speech_output = "Thank you for using the How Can I Help? skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "How Can I Help?"
    speech_output = "Welcome to the Alexa How Can I Help? skill. " \
                    "Let's do something good together. " \
                    "You can ask me for event categories, or " \
                    "ask me for events by category or events by date."
    reprompt_text = "Please ask me for an event category, " \
                    "for example, you can say, " \
                    "What are the categories?"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_categories():
    session_attributes = {}
    card_title = "How Can I Help? Categories"
    reprompt_text = ""
    should_end_session = False

    dynamo = boto3.resource('dynamodb').Table('Categories')
    categories = dynamo.scan()

    if (categories):
        categories_text = ""

        for category in categories['Items']:
            categories_text += (category['description'] + " \n")

            speech_output = "Here are the categories you can help with: " + categories_text + " n\ "
            reprompt_text = "Would you like to help with one of these categories? " \
                            "You can say, I want to help with animals."
    else:
        speech_output = "There are no categories that match your request."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_events_by_category(category):
    session_attributes = {}
    card_title = "How Can I Help? Events By Category"
    speech_output = ""
    reprompt_text = ""
    should_end_session = False

    dynamo = boto3.resource('dynamodb').Table('Events')

    events = dynamo.query(
        IndexName='category-index',
        KeyConditionExpression=Key('category').eq(category)
    )

    if (events):
        for event in events['Items']:
            speech_output += event['description'] + ' on ' + event['event_date_time'] + ' '
            speech_output += 'by ' + event['organization'] + '\n'
            #reprompt_text = 'Would you like to help with this event?'
    else:
        speech_output = "There are no events that match your request."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_events_by_date():
    session_attributes = {}
    card_title = "How Can I Help? Events By Date"
    speech_output = ""
    reprompt_text = ""
    should_end_session = False

    if "Date" in intent["slots"]:
        date = intent["slots"]["Date"]["value"]
        dynamo = boto3.resource('dynamodb').Table('Events')
        events = lambda x: dynamo.get_item(
            Key={
                    "date": date
            }
        )

        if (events):
            speech_output = "Here are events that you can help with " + today

            for event in events:
                print (event)
                speech_output += event['name'] + ' on ' + event['date']
                speech_output += event['description']
                # reprompt_text = 'Would you like to help with this event?'
        else:
            speech_output = "There are no events that match your request."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_my_events(intent):
    session_attributes = {}
    card_title = "How Can I Help? My Events"
    speech_output = "This feature is not yet supported. " \
                    "Soon you will be able to login with Amazon " \
                    "and save your events."
    reprompt_text = "Would you like to hear about more ways you can help? " \
                    "Try asking about Homeless or Food for example."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_events_near_me(intent):
    session_attributes = {}
    card_title = "How Can I Help? Events Near Me"
    speech_output = "This feature is not yet supported. " \
                    "Soon you will be able to login with Amazon " \
                    "and share your location."
    reprompt_text = "Would you like to hear about more ways you can help? " \
                    "Try asking about Homeless or Food for example."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
