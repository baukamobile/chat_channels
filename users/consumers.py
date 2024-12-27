import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        #self.scope["url_route"]["kwargs"]["room_name"]
        # Получает 'room_name'параметр из маршрута URL,
        # chat/routing.py открывшего соединение WebSocket с потребителем.
        # У каждого потребителя есть область действия ,
        # содержащая информацию о его соединении, включая, в частности, любые
        # позиционные или ключевые аргументы из маршрута URL, а также информацию о
        # текущем аутентифицированном пользователе, если таковой имеется.
        self.room_group_name = f"chat_{self.room_name}"
        #self.room_group_name = f"chat_{self.room_name}"
        # Создает имя группы каналов непосредственно из указанного пользователем имени комнаты, без кавычек или экранирования.
        #Имена групп могут содержать только буквы, цифры,
        # дефисы, подчеркивания или точки. Поэтому этот
        # пример кода не будет работать с именами комнат, которые содержат другие символы.
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
         #async_to_sync(self.channel_layer.group_add)(...)
        #Присоединяется к группе.
        # #Обертка async_to_sync(...)необходима, поскольку ChatConsumer является
        # синхронным WebsocketConsumer, но он вызывает асинхронный метод уровня
        # канала. (Все методы уровня канала являются асинхронными.)
        #Имена групп ограничены только буквами ASCII, цифрами, дефисами и точками
        # и ограничены максимальной длиной 100 в бэкэнде по умолчанию. Поскольку этот
        # код создает имя группы непосредственно из имени комнаты, он завершится ошибкой,
        # если имя комнаты содержит какие-либо символы, недопустимые в имени группы, или превышает ограничение по длине.

        self.accept()
        #self.accept()
        #Принимает соединение WebSocket.
        #Если вы не вызовете accept()внутри connect()метода,
        # то соединение будет отклонено и закрыто. Вы можете захотеть
        # отклонить соединение, например, потому что запрашивающий пользователь
        # не авторизован для выполнения запрошенного действия.

        #Рекомендуется accept()вызывать это действие в качестве последнегоconnect() , если вы решите принять соединение.


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        #async_to_sync(self.channel_layer.group_discard)(...)
# Покидает группу.

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        some_event = 'some event'

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_mess", "message": f"event {some_event},{type(message)}: " +message}
        )
        #async_to_sync(self.channel_layer.group_send)
        # Отправляет событие в группу.
        # Событие имеет специальный 'type'ключ, соответствующий имени метода,
        # который должен быть вызван для потребителей, получающих событие.
        # Этот перевод выполняется путем замены .на _, таким образом,
        # в этом примере chat.message вызывается chat_messageметод.
    # Receive message from room group
    def chat_mess(self, event):
        message = event["message"]
        username = "Adam"

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": f"{username}: "+message}))






