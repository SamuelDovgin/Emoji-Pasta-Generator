import json
import requests

VERIFY_TOKEN = "EmojifyToken"
PAGE_ACCESS_TOKEN = "EAAmr9K7fh7sBAHEZBn2xPqeEQbVvb0glJQifYw100o6HvSKZAZA046Ry4OYHL22UW991xoPgijSFoLOJgZAZCiFEDINGJQmneOJV2nyy4VQGquBntPCQcEoFUMKb3AhgBZAZC6rAyskKZCRSlwP8ZBhDABqBZAnasHH4zUYxRTUmdtMQZDZD"

def callSendAPI(messageData):
  body = json.stringify(messageData)
  path = "graph.facebook.com" + '/v2.6/me/messages?access_token=' + PAGE_ACCESS_TOKEN
  options = {
    'host': "graph.facebook.com",
    'path': path,
    'method': 'POST',
    'headers': {'Content-Type': 'application/json'}
  }
  x = requests.post(path, body)
  console.log(x)

def sendTextMessage(recipientId, messageText):
  messageData = {
    'recipient': {
      'id': recipientId
    },
    'message': {
      'text': messageText
    }
  }
  callSendAPI(messageData)

def receivedMessage(event):
    console.log(event['message'])
  
    senderID = event['sender.id']
    recipientID = event['recipient']['id']
    timeOfMessage = event['timestamp']
    message = event['message']
    #console.log("Received message for user %d and page %d at %d with message:", senderID, recipientID, timeOfMessage);
    #console.log(JSON.stringify(message));
    messageId = message['mid']
    messageText = message['text']
    messageAttachments = message['attachments']
    if messageText:
        # If we receive a text message, check to see if it matches a keyword
        # and send back the example. Otherwise, just echo the text we received.
        """ switch (messageText) {
        case 'generic':
            //sendGenericMessage(senderID);
            break;
        default: """
        sendTextMessage(senderID, messageText)
        #}
    elif messageAttachments:
        sendTextMessage(senderID, "Message with attachment received")

def my_handler(event, context):
    # process GET request
    if(event['queryStringParameters']):
        queryParams = event['queryStringParameters']
    
        rVerifyToken = queryParams['hub.verify_token']
 
        if (rVerifyToken == VERIFY_TOKEN):
            challenge = queryParams['hub.challenge']
            response = {
                'body': challenge,
                'statusCode': 200
            }
            return response
        else:
            response = {
                'body': 'Error, wrong validation token',
                'statusCode': 422
            }
            return response
    # process POST request
    else:
        console.log(event['body'])
        data = json.parse(event['body'])
        # Make sure this is a page subscription
        if (data['object'] == 'page'):
            for i in data['entry']:
                pageID = i['id']
                timeOfEvent = i['time']
                for j in i['messaging']:
                    if j['message']:
                        receivedMessage(j)
                    else:
                        console.log(event['body'])
        response = {
        'body': "ok",
        'statusCode': 200
        }
        return response