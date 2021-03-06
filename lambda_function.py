"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function
import socket


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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

def buildSpeechletResponseWithDirectiveNoIntent():
    print("in buildSpeechletResponseWithDirectiveNoIntent");
    return {
      "outputSpeech" : None,
      "card" : None,
      "directives" : [ {
        "type" : "Dialog.Delegate"
      } ],
      "reprompt" : None,
      "shouldEndSession" : False
    }

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the PVR skill" \
                    "Please tell me a show to record by saying, " \
                    "Record channel number at date time for X number of minutes."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me a show to record by saying, " \
                    "Record channel number at date time for X number of minutes."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Over the Air TV Recorder. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    if 'attributes' in session:
        session_attributes = session['attributes']
    else:
        session_attributes = {}
    should_end_session = False
    
    channelNum = intent['slots']['ChannelNumber']['value']
    duration = intent['slots']['Duration']['value']
    timeRecord = intent['slots']['Time']['value']
    dateRecord = intent['slots']['Date']['value']
    
    HOST = get_IP_address_from_session(intent,session)
    PORT = 9998
    data = ''.join([channelNum,'\n',timeRecord,'\n',dateRecord,'\n',duration,'\n'])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))


    print("Sent:     {}".format(data), end='')

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def set_IP_address(intent, session):
    card_title = intent['name']
    if 'attributes' in session:
        session_attributes = session['attributes']
    else:
        session_attributes = {}
    should_end_session = False
    reprompt_text = None
    
    session_attributes = {'first' : intent['slots']['first']['value'], 'second' : intent['slots']['second']['value'], 'third' : intent['slots']['third']['value'], 'forth' : intent['slots']['forth']['value']}
    speech_output = "Your IP Address has been set"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def get_IP_address_from_session(intent, session):
    
    if session.get('attributes',{}) and 'first' in session.get('attributes',{}):
        IP_address = ''.join((session['attributes']['first'],'.',
            session['attributes']['second'],'.',session['attributes']['third'],'.',
            session['attributes']['forth']))
    else:
        IP_address = 'unknown'
    
    print(''.join(IP_address))

    return IP_address


# --------------- Events ------------------

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
    if 'attributes' in session:
        session_attributes = session['attributes']
    else:
        session_attributes = {}
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    if 'dialogState' in intent_request and intent_request['dialogState'] != 'COMPLETED':
        print('Dialog state started')
        return build_response(session_attributes, buildSpeechletResponseWithDirectiveNoIntent())
    #else:
     #   return get_welcome_response()


    # Dispatch to your skill's intent handlers
    if intent_name == "Record":
        return set_color_in_session(intent, session)
        #return get_IP_address_from_session(intent,session)
    elif intent_name == "IPAddress":
        return set_IP_address(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

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
    #if event['request']['dialogState'] == 'STARTED':
    #    print('Dialog started')
    #elif event['request']['dialogState'] == 'COMPLETED':
    #    print('Dialog completed')

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
