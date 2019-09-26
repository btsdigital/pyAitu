import asyncio
import aiohttp
import json
from typing import Optional, Union, List, Dict
from . import api


class BaseBot:
    def __init__(
            self,
            token: str,
            loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None
    ):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.token = token
        connector = aiohttp.TCPConnector(loop=self.loop)
        self.session = aiohttp.ClientSession(connector=connector, loop=self.loop, json_serialize=json.dumps)

    async def request(self,
                      method: str,
                      data: Optional[Dict] = None) -> Union[List, Dict, bool]:
        return await api.request(session=self.session, token=self.token, method=method, data=data)
