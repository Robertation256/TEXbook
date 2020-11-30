#!/usr/bin/env python

class Event(object):

    def __init__(self, info=None):
        
        self.info = None

    def __get__(self, object, object_type):

        if object is None:
            return self

        elif object is not None:
            return EventHandler(self, object=object)

        
class EventHandler(object):

    def __init__(self, event, object):

        self.event = event
        self.object = object
        self.event_handlers = []

    def add(self, event_handler):

        """
        This function adds a new event handler to the class

        Each event handler must be defined as event_handler(sender, event_arg)
        It can be added simply using the '+=' operator
        """

        self.event_handlers.append(event_handler)
        return self

    
    def remove(self, event_handler):

        """
        This function removes an existing event handler
        It can simply be done via '-=' operator
        """

        self.event_handlers.remove(event_handler)
        return self

    def execute(self, event_arg = None):

        """
        This function executes an event and calls all the event handles
        It can simply be called as EventHanlder object e(event_arg)
        """

        for event_handler in self.event_handlers:
            event_handler(self.object, event_arg)


    __iadd__ = add
    __isub__ = remove
    __call__ = execute


