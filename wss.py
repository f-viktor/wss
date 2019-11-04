#!/bin/python3

import asyncio
import websockets
import queue
from threading import Thread
from datetime import datetime

class WShandler:

    def __init__(self,wss_host,filter=[],pingmsg=None,interval=0.1):
        self.connected=True
        self.senderQ = queue.Queue()
        self.wss_host= wss_host
        self.responses= []
        self.filter=filter
        self.pingmsg=pingmsg
        self.interval=interval
        t=Thread(target=self.start_loop)
        t.start()

    async def close(self):
        self.connected=False
        try:
            await self._websocket.close()
        except Exception as e:
            pass

    # separate thrad so that loop doesnt block execution
    def start_loop(self):
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.handler())

    async def handler(self):
        #if it cannot connect, it crashes = problem
        #create websocket connection
        try:
            self._websocket = await websockets.connect(self.wss_host)
        except Exception:
            print("Connection failed")
            self.connected=False
            return
        #start listener and sender tasks
        consumer_task = asyncio.ensure_future(self.receive())  ## recieve
        producer_task = asyncio.ensure_future(self.send())  ## send
        producer_filler_task = asyncio.ensure_future(self.keepAlive())  ## fill sender queue
        done, pending = await asyncio.wait(
        [consumer_task, producer_task, producer_filler_task],
        return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        #print('### ERROR : Connection to ' + self.wss_host + ' died')
        await self.close()

    # PUT YOUR MESSAGES HERE
    def Q(self,message):
        if self.connected:
            self.senderQ.put(message)
        else:
            raise websockets.exceptions.ConnectionClosed(code=1006,reason="wss.py: Conenction is closed")

    def filterPrint(self,message):
        if not any(line in message for line in self.filter):
            print( message)

    # loop for sending websockets messages queued
    async def send(self):
        while True:
            await asyncio.sleep(self.interval)
            try:
                message = self.senderQ.get(block=False)
                self.filterPrint('> ' + message)
                await self._websocket.send(message)
            except queue.Empty:
                pass
            except websockets.exceptions.ConnectionClosed as e:
                #breaking will terminate the handler, and that will call self.close()
                break


    # loop for reading websockets responses
    async def receive(self):
        while(True):
            try:
                await asyncio.sleep(self.interval)
                message = await self._websocket.recv()
                self.filterPrint('< ' + message)
                self.responses.append(message)
            except websockets.exceptions.ConnectionClosed as e:
                break

    # ping every 25 seconds so the connection does not die
    async def keepAlive(self):
        while(self.pingmsg):
          self.filterPrint('> ' + self.pingmsg)
          try:
            await self._websocket.send(self.pingmsg)
            await asyncio.sleep(25)
          except websockets.exceptions.ConnectionClosed as e:
             break

        while True: # so that thread does not end if ping is not requred
            await asyncio.sleep(300)

    # return all responses that have "contains", can block thread until first valid resp
    def response_has(self,contains,block=False):
        result=[]
        if block:
            while not result:
                for response in self.responses:
                    if contains in response:
                        result.append(response)
        else:
                for response in self.responses:
                    if contains in response:
                        result.append(response)

        return result
