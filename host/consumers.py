import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer

# from .models import Thread, ChatMessage

class PlayerConsumer(AsyncConsumer):   # AsyncConsumer  # AsyncWebsocketConsumer
    async def websocket_connect(self, event):   #Function name is fixed    
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        # other_user = self.scope['url_route']['kwargs']['join']
        # me = self.scope['user']
        # await asyncio.sleep(5)
        await self.send({
            # "type": "websocket.close"
            "type": "websocket.send",
            "text": "Websocket connected",
        })

    async def websocket_receive(self, event):
        print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            dict_data = json.loads(front_text)
            print(dict_data)
            self.sendOnlyAtStart = dict_data.get('sendOnlyAtStart')
            self.username = dict_data.get('username')
            self.room_code = dict_data.get('room_code')
            # self.room_code = room_code
            if self.username is None:        # Host connected
                print("Host connected with details: ", dict_data)
                if self.sendOnlyAtStart == "1":
                    print("Host Started")     #Add name to the players list
                    # Join room group
                    await self.channel_layer.group_add(
                        self.room_code,
                        self.channel_name
                    )
                elif dict_data.get('reset') is not None:
                    print("Reset player ranks")     # Reset Rank List to Empty
                    
                    myResponse = {
                        'info': "reset",
                        # 'username': username,
                        'room_code': self.room_code
                    }
                    await self.channel_layer.group_send(
                        self.room_code,
                        {
                            "type": "message_event",
                            "text": json.dumps(myResponse),
                        }
                    )
                elif dict_data.get('info') == "changed_player_list":
                    print("Changed players list")     # Reset Rank List to Empty
                    
                    myResponse = {
                        'info': "changed_player_list",
                        # 'username': username,
                        'room_code': self.room_code,
                        'new_list': dict_data.get("new_list"),
                    }
                    await self.channel_layer.group_send(
                        self.room_code,
                        {
                            "type": "message_event",
                            "text": json.dumps(myResponse),
                        }
                    )
                elif dict_data.get('info') == "kickPlayer":
                    print("do something when a player is kicked")

            elif len(self.username)>0 :      # Player connected
                if self.sendOnlyAtStart == "1":
                    print(self.username+" has joined the game!")     #Add name to the players list
                    await self.channel_layer.group_add(
                        self.room_code,
                        self.channel_name
                    )
                    myResponse = {
                        'info': "add_new_player",
                        'username': self.username,
                        'room_code': self.room_code
                    }
                    # if 'room_code' in request.session:
                    #     room_code = request.session['room_code']
                    await self.channel_layer.group_send(
                        self.room_code,
                        {
                            "type": "message_event",
                            "text": json.dumps(myResponse),
                        }
                    )
                else:
                    print(self.username+" Buzzed")       # When buzzer is pressed
                    myResponse = {
                        'info': "buzzer_pressed",
                        'username': self.username,
                        'room_code': self.room_code
                    }
                    await self.channel_layer.group_send(
                        self.room_code,
                        {
                            "type": "message_event",
                            "text": json.dumps(myResponse),
                        }
                    )

            
            # if sendOnlyAtStart == "1":
            #     print("Sent only on first connection")
            #     return
            
            # await self.channel_layer.group_add(
            #     room_code,
            #     self.channel_name
            # )
            # print("username: ",username, " Room code: ", room_code)
            # myResponse = {
            #     'info': "all",
            #     'username': username,
            #     'room_code': room_code
            # }
            
            # await self.channel_layer.group_send(
            #     self.room_code,
            #     {
            #         "type": "message_event",
            #         "text": json.dumps(myResponse),
            #     }
            # )
            # await self.send({
            #     "type":"websocket.send",
            #     "text": json.dumps(myResponse),
            # })
    async def message_event(self, event):
        print('message', event)
        await self.send({
            "type": "websocket.send",
            "text": event['text'],
        })
    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
                        self.room_code,
                        self.channel_name
                    )
        print("disconnect", event)

