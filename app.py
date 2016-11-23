#!/usr/bin/env python

import urllib
import json
import os

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
    if req.get("result").get("action") == "send.programme":
        result = req.get("result")
        parameters = result.get("parameters")
        date = parameters.get("date")
        thingstodo = {'2016-11-23':'Go to A, B or C', '2016-11-24':'Do D, E, F', '2016-11-25':'Visit G, H, I'}
        speech = "On " + str(date) + " you could do the following: " + str(thingstodo[date])

    elif req.get("result").get("action") == "spa.info":
        result = req.get("result")
        parameters = result.get("parameters")
        speech = "Our spa has the following to offer: nice massages, fango and so on..."
    else
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
