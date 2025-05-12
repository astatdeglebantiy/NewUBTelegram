from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from typing import Callable

class Manager:
    def __init__(self, client: Client):
        self.client = client
        self.handlers: dict[str, any] = {}

    def register_handler(self, name: str, func: Callable, flt=None, group: int = 0):
        if name in self.handlers:
            return
        flt = flt or filters.text
        handler = self.client.add_handler(MessageHandler(func, flt), group=group)
        self.handlers[name] = (handler, group) if group != 0 else handler

    def remove_handler(self, name: str):
        h = self.handlers.pop(name)
        if isinstance(h, tuple):
            handler, grp = h
            self.client.remove_handler(handler, grp)
        else:
            self.client.remove_handler(h)

    def clear_handlers(self):
        for name in list(self.handlers):
            self.remove_handler(name)

    def list_handlers(self):
        handlers_list = []
        for handler in self.handlers:
            handlers_list.append(handler)
        return handlers_list
