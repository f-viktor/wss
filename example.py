#!/bin/python

import json
from wstool import WShandler

host="wss://somendpoint.com/websockets"


if __name__ == "__main__":
   grep=['mobileSOCall','setPerfBirthday']

    wss=WShandler(host,filter=grep,pingmsg="are_you_there_m8?")
    wss.Q('{"hello":"hi"}')
    wss.Q('{"hardest_question":"are you worthy to build the temple}')


    userid_response=wss.response_has("answer",block=True)[0]
    print(json.loads(userid_response)['answer'])

