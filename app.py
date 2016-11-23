#!/usr/bin/env python

import urllib
import json
import os
import time

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    thingstodo = {'2016-11-23':'Go to A, B or C', 
                  '2016-11-24':'You should visit D, E, or F. They have great X!', 
                  '2016-11-25':'Visit G, H, I',
                  '2016-11-26':'Go to J or K',
                  '2016-11-27':'You could visit our nice spa or have a walk at the beach!'}

    if req.get("result").get("action") == "send.programme":
        result = req.get("result")
        parameters = result.get("parameters")
        date = parameters.get("date")
        speech = "On " + str(date) + " you could do the following: " + str(thingstodo[date])

    elif req.get("result").get("action") == "spa.info":
        result = req.get("result")
        parameters = result.get("parameters")
        speech = "Our spa has the following to offer: nice massages, fango and so on... Should I reserve an appointment at the spa for you?"
        
    elif req.get("result").get("action") == "send.programme.today":
        result = req.get("result")
        parameters = result.get("parameters")
        date = time.strftime("%Y-%m-%d")
        speech = "Today you could do the following: "+str(thingstodo[date])
        
    else:
        return{}    
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "ptuidb-thingstodo"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
