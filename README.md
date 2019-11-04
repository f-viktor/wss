# wstool_python

you can preset the chain of websockets messages you want to send, so that you do not have to copy paste every time.

## howto
create a `WShandler` object and tell it where to connect e.g.:
```
wss = WShandler(wss://endpoint.com/)
```

you can also set up a balacklist of responses with the filter attribute to surpress noise.
This is because grep sometimes doesn't work.
```
blocklist=['partialstring','part of a response]
wss = WShandler(wss://endpoint.com/,filter=blocklist)

```

queue up your messages with `wss.Q(message)` as in e.g.:

```
wss.Q('{"event":"client_hello"}')
wss.Q('{"event":"client_do_smthng"}')
wss.Q('{"event":"client_bye"}')
```
The oldest element of the queue will be sent every 0.1 second.

You query all the responses directly via the `wss.responses` variable

You can look for messages with a specific substring via `wss.response_has(substring)'

You can block execution until a message with a specific substring has arrived as:

```
print("do something")
userId_response = wss.response_has('userId',block=True)[0]
print(json.loads(userId_response)['userId'])
```
useful when a followup message requires part of the answer


