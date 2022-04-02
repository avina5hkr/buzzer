import asyncio
from cgitb import text
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from core.settings import ACTIVE_ROOMS

class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_type = self.scope['url_route']['kwargs']['user_type']
        self.username = (self.scope['url_route']['kwargs']).get('username')
        # print(self.username)
        print(self.user_type, "started")
        self.room_group_name = 'game_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        if self.user_type == "player":
            print(self.username, "with channel name: ", self.channel_name," has joined the game!")     #Add name to the players list
            
            myResponse = {
                        'info': "add_new_player",
                        'username': self.username,
                        'room_code': self.room_name,
                        'channel_name': self.channel_name
                    }
                    # if 'room_code' in request.session:
                    #     room_code = request.session['room_code']
            await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "message_event",
                            "message": json.dumps(myResponse),
                        }
                    )
        # print("geting out of connect")

        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        if self.user_type=="host" and self.room_name in ACTIVE_ROOMS:
            ACTIVE_ROOMS.remove(self.room_name)
            print(self.room_name, "host disconneted so removing")
            # print("Active Rooms:", ACTIVE_ROOMS)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        print(text_data_json)
        self.user_type = self.scope['url_route']['kwargs']['user_type']
        self.username = (self.scope['url_route']['kwargs']).get('username')
        
        if self.user_type == "host":
            # if text_data_json.get('sendOnlyAtStart'):
                
            if text_data_json.get('reset') is not None:
                    print("Reset player ranks")     # Reset Rank List to Empty
                    
                    myResponse = {
                        'info': "reset",
                        'room_code': self.room_name
                    }
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "message_event",
                            "message": json.dumps(myResponse),
                        }
                    )
            elif text_data_json.get('info') == "changed_player_list":
                    print("Changed players list")     # Reset Rank List to Empty
                    
                    myResponse = {
                        'info': "changed_player_list",
                        # 'username': username,
                        'room_code': self.room_name,
                        'new_list': text_data_json.get("new_list"),
                    }
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "message_event",
                            "message": json.dumps(myResponse),
                        }
                    )
            elif text_data_json.get('info') == "kickPlayer":
                    
                    if text_data_json.get('id'):
                        await self.channel_layer.group_discard(
                        self.room_group_name,
                        text_data_json.get('id')
                        )
                        print("player kicked out!!!")
            
            # await self.channel_layer.group_send(
            # self.room_group_name,
            # {
            #     'type': 'message_event',
            #     'message': "message"
            # }
        # )
        elif self.user_type == "player":
            if text_data_json.get('sendOnlyAtStart')=='1':
                myResponse = {
                        'info': "add_new_player",
                        'username': self.username,
                        'room_code': self.room_name
                    }
                # print(myResponse)
                #     # if 'room_code' in request.session:
                #     #     room_code = request.session['room_code']
                # await self.channel_layer.group_send(
                #         self.room_group_name,
                #         {
                #             "type": "message_event",
                #             "text": json.dumps(myResponse),
                #         }
                #     )
            else:
                print(self.username+" Buzzed")       # When buzzer is pressed
                myResponse = {
                        'info': "buzzer_pressed",
                        'username': self.username,
                    }
                await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "message_event",
                            "message": json.dumps(myResponse),
                        }
                    )
                
                
        
        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'message_event',
        #         'message': "message"
        #     }
        # )

    # Receive message from room group
    async def message_event(self, event):
        message = event.get('message')
        # print(message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            # 'type': 'websocket.send',
            'message': message
        }))
