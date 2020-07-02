'use strict';
var VERIFY_TOKEN = "EmojifyToken";

var https = require('https');
var PAGE_ACCESS_TOKEN = "EAAmr9K7fh7sBAHEZBn2xPqeEQbVvb0glJQifYw100o6HvSKZAZA046Ry4OYHL22UW991xoPgijSFoLOJgZAZCiFEDINGJQmneOJV2nyy4VQGquBntPCQcEoFUMKb3AhgBZAZC6rAyskKZCRSlwP8ZBhDABqBZAnasHH4zUYxRTUmdtMQZDZD";
exports.handler = (event, context, callback) => {
    
  // process GET request
  if(event.queryStringParameters){
    var queryParams = event.queryStringParameters;
 
    var rVerifyToken = queryParams['hub.verify_token']
 
    if (rVerifyToken === VERIFY_TOKEN) {
      var challenge = queryParams['hub.challenge']
      
      var response = {
        'body': challenge,
        'statusCode': 200
      };
      
      callback(null, response);
    }else{
      var response = {
        'body': 'Error, wrong validation token',
        'statusCode': 422
      };
      
      callback(null, response);
    }
  
  // process POST request
  }else{
    var data = JSON.parse(event.body);
     
    // Make sure this is a page subscription
    if (data.object === 'page') {
    // Iterate over each entry - there may be multiple if batched
    data.entry.forEach(function(entry) {
        var pageID = entry.id;
        var timeOfEvent = entry.time;
        // Iterate over each messaging event
        entry.messaging.forEach(function(msg) {
          if (msg.message) {
            receivedMessage(msg);
          } else {
            console.log("Webhook received unknown event: ", event);
          }
        });
    });
    
    }
    // Assume all went well.
    //
    // You must send back a 200, within 20 seconds, to let us know
    // you've successfully received the callback. Otherwise, the request
    // will time out and we will keep trying to resend.
    var response = {
      'body': "ok",
      'statusCode': 200
    };
      
    callback(null, response);
  }
}
function receivedMessage(event) {
  console.log("Message data: ", event.message);
  
  var senderID = event.sender.id;
  var recipientID = event.recipient.id;
  var timeOfMessage = event.timestamp;
  var message = event.message;
  console.log("Received message for user %d and page %d at %d with message:", senderID, recipientID, timeOfMessage);
  console.log(JSON.stringify(message));
  var messageId = message.mid;
  var messageText = message.text;
  var messageAttachments = message.attachments;
  if (messageText) {
    // If we receive a text message, check to see if it matches a keyword
    // and send back the example. Otherwise, just echo the text we received.
    switch (messageText) {
      case 'generic':
        //sendGenericMessage(senderID);
        break;
      default:
        sendTextMessage(senderID, messageText);
    }
  } else if (messageAttachments) {
    sendTextMessage(senderID, "Message with attachment received");
  }
}

function find_punct_ending_index(input_string){
    var punctuation_start = -1
    var punctuation_adj = false
    var all_punct = "[\\.,-/#!$%^&*;:{}=-_`~()@+?><[]+]\"\'"
    var string_len_range = [...Array(input_string.length).keys()]
    string_len_range.forEach(function(i) {
      if (all_punct.includes(input_string.charAt(i)) && input_string.charAt(i) !== "\'"){
        if (!punctuation_adj){
          punctuation_start = i 
        }
        punctuation_adj = true
      } else {
        punctuation_start = -1
        punctuation_adj = false
      }
    });
    if (punctuation_adj){
      return punctuation_start 
    } else{
      return null 
    }
}

function emoji_prob_picker(input_string, emoji_map){
    var total_prob_counter = 0
    var rand_value = Math.random()
    if (input_string in emoji_map){
      var keys = Object.keys(emoji_map[input_string])
      for (var key of keys){
        total_prob_counter += emoji_map[input_string][key];
            if (rand_value <= total_prob_counter){
              return key
            }
      }
    }
    return ""
}


function emoji_pasta_maker(raw_string, emoji_prob_map){
    var raw_string_new_line = raw_string.replace("\n", " \n")
    var raw_string_split_upper = raw_string_new_line.split(" ")
    var raw_string_split = []
    for (var string_upper of raw_string_split_upper){
        if (string_upper.charAt(0) == "\n"){
          raw_string_split.push("\n")
          raw_string_split.push(string_upper.substring(1).toLowerCase())
        } else{
           raw_string_split.push(string_upper.toLowerCase()) 
        }
    }
    var normalized_string_list = []
    var emoji_list = []
    var final_emoji_pasta = ""
    var string_len_range = [...Array(raw_string_split.length).keys()]
    string_len_range.forEach(function(i) {
        var normalized_string = raw_string_split[i].replace(/[.,\/#!$%\^&\*;:{}=\-_`~()\']/g,"")
        normalized_string_list.push(normalized_string)
    });
    normalized_string_list.forEach(function(i) {
        emoji_list.push(emoji_prob_picker(i,emoji_prob_map))
    });
    var string_len_range2 = [...Array(raw_string_split.length).keys()]
    string_len_range2.forEach(function(i) {
        if (emoji_list[i] !== ""){
            var punct_starting_index = find_punct_ending_index(raw_string_split[i])
            if (punct_starting_index){
                final_emoji_pasta += + raw_string_split[i].substring(0,punct_starting_index) + " " + emoji_list[i] + raw_string_split[i].substring(punct_starting_index) + " "
            } else{    
                final_emoji_pasta += raw_string_split[i] + " " + emoji_list[i] + " "
              }
            }
        else{
            final_emoji_pasta += raw_string_split[i] + " "
        }
    });
    return final_emoji_pasta
}

function parse_emoji_mapping(emoji_dictionary){
  //var result = JSON.parse(jsonResult);
}


function sendTextMessage(recipientId, messageText) {
  var emoji_message = emoji_pasta_maker(messageText,maptest)
  var messageData = {
    recipient: {
      id: recipientId
    },
    message: {
      text: emoji_message
    }
  };
  callSendAPI(messageData);
}
function callSendAPI(messageData) {
  var body = JSON.stringify(messageData);
  var path = '/v2.6/me/messages?access_token=' + PAGE_ACCESS_TOKEN;
  var options = {
    host: "graph.facebook.com",
    path: path,
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
  };
  var callback = function(response) {
    var str = ''
    response.on('data', function (chunk) {
      str += chunk;
    });
    response.on('end', function () {
 
    });
  }
  var req = https.request(options, callback);
  req.on('error', function(e) {
    console.log('problem with request: '+ e);
  });
 
  req.write(body);
  req.end();
}
