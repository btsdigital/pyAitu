import logging
import aiohttp
import json
import os
from http import HTTPStatus
from ..models import Bot

log = logging.getLogger('pyAitu')

if os.getenv("DEV", "FALSE") == "TRUE":
    BASE_URL = "https://botapi.dev.btsdapps.net/bot/v1/"
else:
    BASE_URL = "https://botapi.btsdapps.net/bot/v1/"

API_URL = BASE_URL + "updates"
FILE_UPLOAD_URL = BASE_URL + "upload/"
FILE_DOWNLOAD_URL = BASE_URL + "download/"
WEBHOOK_INFO_URL = BASE_URL + "webhook/"


def _compose_data(params=None, files=None):
    data = aiohttp.formdata.FormData(quote_fields=False)
    if params:
        for key, value in params.items():
            data.add_field(key, str(value))

    if files:
        for key, f in files.items():
            data.add_field('key', open(f, 'rb'), filename=os.path.basename(f), content_type='application/octet-stream')

    return data


async def request(session, token, method, data=None, proxy=None, files=None, **kwargs) -> bool or dict:
    log.debug(f"Making request {method}")

    if files and method == "UploadFile":
        data = _compose_data(data, files)
        try:
            async with session.post(FILE_UPLOAD_URL, data=data, proxy=proxy, headers={"X-BOT-TOKEN": token}, **kwargs) as response:
                return await _check_result(method, response)
        except aiohttp.ClientError as e:
            raise Exception(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")
    elif method in ["SetWebhook", "GetWebhook", "DeleteWebhook"]:
        if method == "GetWebhook":
            try:
                async with session.get(WEBHOOK_INFO_URL, proxy=proxy, headers={"X-BOT-TOKEN": token}, **kwargs) as response:
                    return await _check_result(method, response)
            except aiohttp.ClientError as e:
                raise Exception(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")
        elif method == "SetWebhook":
            try:
                async with session.post(WEBHOOK_INFO_URL, proxy=proxy, json=data, headers={"X-BOT-TOKEN": token}, **kwargs) \
                        as response:
                    return await _check_result(method, response)
            except aiohttp.ClientError as e:
                raise Exception(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")
        elif method == "DeleteWebhook":
            try:
                async with session.delete(WEBHOOK_INFO_URL, proxy=proxy, headers={"X-BOT-TOKEN": token}, **kwargs) as response:
                    return await _check_result(method, response)
            except aiohttp.ClientError as e:
                raise Exception(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")
    else:
        try:
            if method == "GetUpdates":
                async with session.get(API_URL, proxy=proxy, headers={"X-BOT-TOKEN": token}, **kwargs) as response:
                    return await _check_result(method, response)
            elif method == "getMe":
                async with session.get(BASE_URL+method, proxy=proxy, headers={"X-BOT-TOKEN": token}, **kwargs) as response:
                    json_object =  await _check_result(method, response)
                    return Bot(json_object)
            else:
                async with session.post(API_URL, proxy=proxy, json=data, headers={"X-BOT-TOKEN": token}, **kwargs) as response:
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

    if result_json.get('error') is not None:
        error = str(result_json.get('error'))
        message = str(result_json.get('message'))
        status = response.status
        log.error(f' - {status}: {error} - {message}')

    description = result_json.get('description') or body
    if HTTPStatus.OK <= response.status <= HTTPStatus.IM_USED:
        return result_json
