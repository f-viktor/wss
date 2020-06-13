# wstool_python

Send a preset list of websocket messages simply.

## howto
create a `WShandler` object and tell it where to connect e.g.:
```
wss = WShandler("wss://endpoint.com/")
```

you can also set up a blacklist of responses with the filter attribute to surpress noise.

```
blocklist=['partialstring','part of a response']
wss = WShandler("wss://endpoint.com/",filter=blocklist)

```

queue up your messages with `wss.Q(message)`  e.g.:

```
wss.Q('{"event":"client_hello"}')
wss.Q('{"event":"client_do_smthng"}')
wss.Q('{"event":"client_bye"}')
```
The oldest element of the queue will be sent every 0.1 seconds.

You can query all the responses directly via the `wss.responses` variable

You can look for messages with a specific substring via `wss.response_has(substring)'

You can block execution until a message with a specific substring has arrived as:

```
print("do something")
userId_response = wss.response_has('userId',block=True)[0]
print(json.loads(userId_response)['userId'])
```
useful when a followup message requires part of the answer


