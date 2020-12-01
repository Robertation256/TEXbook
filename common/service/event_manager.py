from common.handlers import email_handler, notification_handler


class EventManager():
    def __init__(self):
        self.__handlers = [
            email_handler.EmailHandler(),
            notification_handler.NotificationHandler()
        ]

    def publish(self, event):
        for handler in self.__handlers:
            handler.handle(event)
