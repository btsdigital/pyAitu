import logging
import aiohttp
import json
from http import HTTPStatus

log = logging.getLogger('pyAitu')

API_URL = "https://messapi.btsdapps.net/bot/v1/updates/"


async def request(session, token, method, data=None, **kwargs) -> bool or dict:
    log.debug(f"Making request {method}")

    if method == "UploadFile":
        print('upload file')
    else:
        try:
            if method == "GetUpdates":
                async with session.get(API_URL, headers={"X-BOT-TOKEN": token}, **kwargs) as response:
                    return await _check_result(method, response)
            else:
                async with session.post(API_URL, json=data, headers={"X-BOT-TOKEN": token}, **kwargs) as response:
                    return await _check_result(method, response)
        except aiohttp.ClientError as e:
            raise Exception(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")


async def _check_result(method_name, response):
    body = await response.text()
    log.debug(f"Response for {method_name}: [{response.status}] {body}")

    if response.content_type != 'application/json':
        raise Exception(f"Invalid response with content type {response.content_type}: \"{body}\"")

    try:
        result_json = await response.json(loads=json.loads)
    except ValueError:
        result_json = {}

    description = result_json.get('description') or body
    if HTTPStatus.OK <= response.status <= HTTPStatus.IM_USED:
        return result_json
