from typing import Iterable


class MiddlewareManager:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.loop = dispatcher.loop
        self.bot = dispatcher.bot
        self.applications = []

    async def trigger(self, action: str, args: Iterable):
        for app in self.applications:
            await app.trigger(action,args)