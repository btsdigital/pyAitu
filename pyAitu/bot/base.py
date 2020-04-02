import asyncio
import aiohttp
import json
import io
from typing import Optional, Union, List, Dict
from . import api


class BaseBot:
    def __init__(
            self,
            token: str,
            proxy: str = None,
            loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None
    ):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.token = token
        self.proxy = proxy
        connector = aiohttp.TCPConnector(loop=self.loop, ssl=False)
        self.session = aiohttp.ClientSession(connector=connector, loop=self.loop, json_serialize=json.dumps)
        self.local_id_to_message_id = {}

    async def request(self,
                      method: str,
                      data: Optional[Dict] = None,
                      files: Optional[Dict] = None) -> Union[List, Dict, bool]:
        return await api.request(
            session=self.session, token=self.token, method=method, data=data, proxy=self.proxy, files=files)

    async def download_file(
            self,
            file_id: str,
            destination=None,
            chunk_size: int = 65536,
            seek: bool = True
    ):
        if destination is None:
            destination = io.BytesIO()

        url = "{}?fileId={}".format(api.FILE_DOWNLOAD_URL, file_id)
        destination_ = destination if isinstance(destination, io.IOBase) else open(destination, 'wb')
        async with self.session.get(url, headers={"X-BOT-TOKEN": self.token}) as response:
            while True:
                chunk = await response.content.read(chunk_size)
                if not chunk:
                    break
                destination_.write(chunk)
                destination_.flush()
        if seek:
            destination_.seek(0)
        return destination_
