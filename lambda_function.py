"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from twilio.rest import TwilioRestClient


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "MyProblemIsIntent":
        return set_problem(intent, session)
    elif intent_name == "WhatsMyProblemIntent": 
        return get_help(intent, session)
    elif intent_name == "ContactIntent":
        return contact(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hi, I'm Alexa!" \
                    "How can I help you today?" \
                    "what can I do for you?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Are you in danger? Do you want help?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
    
def contact(intent, session):
	card_title = intent['name']
	session_attributes = {}
	reprompt_text = None
	account_sid = "AC39d9722bca359c3885bd8e876492859d"
	auth_token  = "222f8028aa78ffbdecbb558badf6db93"
	client = TwilioRestClient(account_sid, auth_token)
	speech_output = "Something went wrong, sorry."
	should_end_session = True
	try:
		message = client.messages.create(body="Save me it's an emergency #mhacks", 
		to="+16478367351",    # Replace with your phone number
	        from_="+15675100423") # Replace with your Twilio number
		print(message.sid)
		speech_output = "I contacted your physician"
	except twilio.TwilioRestException as e:
		print(e)
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))

def get_help(intent, session):
    card_title = intent['name']
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    
    if "Problems" in session.get('attributes', {}):
        problem = session['attributes']['Problems']
        speech_output = "Your problem is " + problem   
    else:
        speech_output = "I'm not sure what your problem is. You can tell me your problem"
    #

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
        
def set_problem(intent, session): 
    #sets what kind of problem is going on  
    card_title = intent['name'] 
    session_attributes = {}
    should_end_session = False 
    
    if 'Problems' in intent['slots']: 
        problem = intent['slots']['Problems']['value'] 
        session_attributes = create_problem_attributes(problem)
        speech_output = "Okay, I see you're having a" + problem + "today"
        print(problem)
        reprompt_text = "You can tell me your problem. I got your back"
                        
    else: 
        speech_output = "So you're not having" + problem + "today?"
        reprompt_text = "I'm not quite sure what the problem is. Let me know how I can help" 
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def create_problem_attributes(problem): 
    return {"Problems": problem}
    
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
